import os
import subprocess
import sys
from pathlib import Path
import shutil

def clear_directory(directory: Path) -> None:
    """Clear generated protobuf files from directory."""
    if directory.exists():
        for file in directory.glob('*'):
            if file.is_file() and (file.suffix in ['.py', '.pyi'] or file.name == '__init__.py'):
                file.unlink()
        print(f"Cleared existing generated files in {directory}")

def generate_python_proto():
    try:
        # Get absolute paths
        root_dir = Path(__file__).parent.parent.absolute()
        proto_dir = root_dir / 'proto'
        output_dir = root_dir / 'karna-python-backend' / 'generated'
        
        # Clear and recreate output directory
        clear_directory(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get all proto files
        proto_files = list(proto_dir.glob('*.proto'))
        
        if not proto_files:
            print("No .proto files found in proto directory!", file=sys.stderr)
            sys.exit(1)
        
        # Generate Python code and type stubs for each proto file
        for proto_file in proto_files:
            subprocess.run([
                sys.executable,
                '-m',
                'grpc_tools.protoc',
                f'--proto_path={proto_dir}',
                f'--python_out={output_dir}',
                f'--mypy_out={output_dir}',
                str(proto_file)
            ], check=True)
            print(f"Generated code for {proto_file.name}")
        
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