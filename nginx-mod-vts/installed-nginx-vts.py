#!/usr/bin/env python3
"""Exercise a VTS module with a real nginx worker and its JSON status endpoint."""
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

binary = shutil.which('nginx') or '/usr/sbin/nginx'
module = Path(os.environ.get('NGINX_VTS_MODULE',
                             '/usr/lib64/nginx/modules/ngx_http_vhost_traffic_status_module.so')).resolve()
expected = os.environ.get('NGINX_EXPECTED_VERSION', '1.30.7')
assert module.is_file(), module
with socket.socket() as listener:
    listener.bind(('127.0.0.1', 0))
    port = listener.getsockname()[1]
with tempfile.TemporaryDirectory(prefix='nginx-vts-test-') as directory:
    root = Path(directory)
    conf = root / 'nginx.conf'
    conf.write_text(f'''load_module "{module}";
worker_processes 1;
pid "{root}/nginx.pid";
error_log "{root}/error.log" info;
events {{ worker_connections 128; }}
http {{
    access_log off;
    client_body_temp_path "{root}/client_body";
    proxy_temp_path "{root}/proxy";
    fastcgi_temp_path "{root}/fastcgi";
    uwsgi_temp_path "{root}/uwsgi";
    scgi_temp_path "{root}/scgi";
    vhost_traffic_status_zone;
    server {{
        listen 127.0.0.1:{port};
        server_name localhost;
        location /hit {{ return 200 "vts-test\\n"; }}
        location /status {{
            vhost_traffic_status_display;
            vhost_traffic_status_display_format json;
        }}
    }}
}}
''')
    args = [binary, '-p', directory + '/', '-e', str(root / 'error.log'), '-c', str(conf)]
    subprocess.run(args + ['-t'], check=True)
    process = subprocess.Popen(args + ['-g', 'daemon off;'],
                               stdout=subprocess.DEVNULL)
    try:
        url = f'http://127.0.0.1:{port}'
        for attempt in range(100):
            if process.poll() is not None:
                raise RuntimeError('nginx exited before serving requests')
            try:
                with urllib.request.urlopen(url + '/hit', timeout=1) as response:
                    assert response.read() == b'vts-test\n'
                break
            except urllib.error.URLError:
                time.sleep(0.1)
        else:
            raise RuntimeError('nginx did not start listening')
        for _ in range(5):
            with urllib.request.urlopen(url + '/hit', timeout=5) as response:
                assert response.status == 200
        with urllib.request.urlopen(url + '/status', timeout=5) as response:
            data = json.load(response)
        assert data['nginxVersion'] == expected, data['nginxVersion']
        assert data['serverZones']['*']['requestCounter'] >= 6, data['serverZones']
        assert data['serverZones']['*']['responses']['2xx'] >= 6, data['serverZones']
        print(f'PASS: VTS JSON status and request counters on nginx {expected}')
    except BaseException:
        if (root / 'error.log').exists():
            print((root / 'error.log').read_text())
        raise
    finally:
        if process.poll() is None:
            process.send_signal(signal.SIGQUIT)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                raise
