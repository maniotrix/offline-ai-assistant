import os
import subprocess
import sys
from pathlib import Path
import shutil
import re

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
        
def fix_proto_imports():
    """Fix import statements in generated protobuf files."""
    # Get the path to the generated directory
    root_dir = Path(__file__).parent.parent
    generated_dir = root_dir / 'karna-python-backend' / 'generated'
    
    # Get all the generated protobuf files
    proto_files = list(generated_dir.glob('*_pb2.py'))
    
    print(f"Found {len(proto_files)} protobuf files in {generated_dir}")
    
    # Regular expression to match import statements for other protobuf files
    import_pattern = re.compile(r'import\s+([a-zA-Z0-9_]+_pb2)\s+as\s+([a-zA-Z0-9_]+)')
    
    # Fix imports in each file
    for proto_file in proto_files:
        print(f"Processing {proto_file.name}...")
        
        # Read the file content
        with open(proto_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace import statements
        modified_content = import_pattern.sub(r'from . import \1 as \2', content)
        
        # Write the modified content back to the file
        if content != modified_content:
            with open(proto_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            print(f"  Fixed imports in {proto_file.name}")
        else:
            print(f"  No imports to fix in {proto_file.name}")
    
    print("Done fixing proto imports")
    
def verify_imports():
    """Verify that the generated protobuf files can be imported correctly."""
    root_dir = Path(__file__).parent.parent
    backend_dir = root_dir / 'karna-python-backend'
    
    # Create __init__.py in the backend directory if it doesn't exist
    (backend_dir / '__init__.py').touch(exist_ok=True)
    
    # Store current directory and path
    current_dir = os.getcwd()
    original_path = sys.path.copy()
    
    try:
        # Change to root directory and set up Python path
        os.chdir(root_dir)
        sys.path.insert(0, str(root_dir / 'karna-python-backend'))
        
        from generated.vision_detect_pb2 import ( # type: ignore
            VisionDetectRPCRequest,
            VisionDetectRPCResponse,
            GetResultsRequest,
            UpdateResultsRequest,
            VisionDetectResultsList,
            VisionDetectResultModel,
            BoundingBox,
        )
        print("✓ Protobuf imports verified successfully!")
        return True
    except ImportError as e:
        print(f"✗ Import verification failed: {e}")
        return False
    finally:
        # Restore original directory and path
        os.chdir(current_dir)
        sys.path = original_path

if __name__ == '__main__':
    generate_python_proto()
    fix_proto_imports()
    verify_imports()