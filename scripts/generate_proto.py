import os
import subprocess
import sys
from pathlib import Path

def generate_python_proto():
    try:
        # Get absolute paths
        root_dir = Path(__file__).parent.parent.absolute()
        proto_dir = root_dir / 'proto'
        output_dir = root_dir / 'karna-python-backend' / 'generated'
        proto_file = proto_dir / 'messages.proto'
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate Python code and type stubs
        subprocess.run([
            sys.executable,
            '-m',
            'grpc_tools.protoc',
            f'--proto_path={proto_dir}',
            f'--python_out={output_dir}',
            f'--mypy_out={output_dir}',
            str(proto_file)
        ], check=True)
        
        print(f"Successfully generated Python protobuf code and type stubs in {output_dir}")
        
        # Create __init__.py
        init_file = output_dir / '__init__.py'
        init_file.touch()
            
    except subprocess.CalledProcessError as e:
        print(f"Error generating protobuf code: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    generate_python_proto()