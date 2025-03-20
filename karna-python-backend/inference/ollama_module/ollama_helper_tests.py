#  add karna-python-backend to the path
import sys
sys.path.append('C:/Users/Prince/Documents/GitHub/Proejct-Karna/offline-ai-assistant/karna-python-backend')

from importlib import reload  # Not needed in Python 2
import logging
reload(logging)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO, datefmt='%I:%M:%S')

logger = logging.getLogger(__name__)

import os
import json

from pathlib import Path
from datetime import datetime
from config.paths import workspace_data_dir, workspace_dir


from ollama_helper import *

if __name__ == "__main__":
    # Test functions for LLM
    def test_regular_generation():
        """Test regular (non-streaming) LLM generation"""
        test_prompt = "Explain how to make a cup of coffee in three steps."
        test_model = "smollm2"
        
        print(f"Testing regular LLM generation with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        
        try:
            response = llm_generate(prompt=test_prompt, model=test_model)
            print("\nResponse:")
            print(response.get("response", "No response found"))
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def test_streaming_generation():
        """Test streaming LLM generation (collected response)"""
        test_prompt = "Write a short poem about artificial intelligence."
        test_model = "smollm2"
        
        print(f"\nTesting streaming LLM generation with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        
        try:
            response = llm_generate(prompt=test_prompt, model=test_model, stream=True)
            print("\nStreamed Response (collected):")
            print(response.get("response", "No response found"))
        except Exception as e:
            print(f"Error: {str(e)}")
            
    def test_real_time_streaming(use_system_prompt=True):
        """Test real-time streaming where chunks are displayed as they arrive"""
        test_prompt = "Tell me a short story about a robot learning to feel emotions."
        test_model = "smollm2"
        
        print(f"\nTesting real-time streaming with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        
        # Define system prompt if enabled
        system_prompt = None
        if use_system_prompt:
            system_prompt = "You are a creative storyteller from India, specialized in emotional narratives about robots and AI."
            print(f"Using system prompt: {system_prompt}")
        
        try:
            stream_llm_generate(prompt=test_prompt, model=test_model, system=system_prompt)
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Test functions for VLM
    def test_regular_vlm_generation():
        """Test regular (non-streaming) VLM generation"""
        test_prompt = "What can you see in this image?"
        # Use absolute path to ensure the file is found
        test_image = str(Path(__file__).parent / "test.png")
        test_model = "granite3.2-vision:latest"
        
        print(f"\nTesting regular VLM generation with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        print(f"Image: {test_image}")
        
        try:
            response = vlm_generate(prompt=test_prompt, image_path=test_image, model=test_model)
            print("\nVLM Response:")
            print(response.get("response", "No response found"))
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def test_streaming_vlm_generation():
        """Test streaming VLM generation (collected response)"""
        test_prompt = "Describe this image in detail."
        # Use absolute path to ensure the file is found
        test_image = str(Path(__file__).parent / "test.png")
        test_model = "granite3.2-vision:latest"
        
        print(f"\nTesting streaming VLM generation with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        print(f"Image: {test_image}")
        
        try:
            response = vlm_generate(prompt=test_prompt, image_path=test_image, model=test_model, stream=True)
            print("\nStreamed VLM Response (collected):")
            print(response.get("response", "No response found"))
        except Exception as e:
            print(f"Error: {str(e)}")
            
    def test_real_time_vlm_streaming(use_system_prompt=True):
        """Test real-time VLM streaming where chunks are displayed as they arrive"""
        test_prompt = "Find the bounding box coordinates of the open requests and output as a json object"
        # Use absolute path to ensure the file is found
        test_image = str(Path(__file__).parent / "test.png")
        test_model = "granite3.2-vision:latest"
        
        print(f"\nTesting real-time VLM streaming with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        print(f"Image: {test_image}")
        
        # Define system prompt if enabled
        system_prompt = None
        if use_system_prompt:
            system_prompt = """You are a good webpage screenshot reader. 
            You will be given a screenshot of a webpage and you properly analyse the image before answering the user's question."""
            print(f"Using system prompt: {system_prompt}")
        
        try:
            stream_vlm_generate(prompt=test_prompt, image_path=test_image, model=test_model, system=system_prompt)
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Test functions for continuous chat streaming
    def test_continuous_chat_streaming():
        """Test continuous chat streaming with conversation history using runtime user input"""
        test_model = "smollm2"
        system_prompt = "You are a helpful, friendly AI assistant."
        
        print("\nContext Retention Options:")
        print("1. Full context retention (default)")
        print("2. Only retain user messages")
        print("3. Only retain assistant responses")
        print("4. No context retention (stateless)")
        
        try:
            choice = int(input("\nSelect an option (1-4): "))
            
            include_user = True
            include_assistant = True
            
            if choice == 2:
                include_assistant = False
            elif choice == 3:
                include_user = False
            elif choice == 4:
                include_user = False
                include_assistant = False
                
            # Call interactive chat with selected options
            interactive_chat_session(
                model=test_model,
                system_prompt=system_prompt,
                include_user_messages=include_user,
                include_assistant_responses=include_assistant
            )
        except ValueError:
            print("Invalid choice. Using default (full context retention).")
            interactive_chat_session(
                model=test_model,
                system_prompt=system_prompt
            )
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Test function for continuous VLM chat streaming
    def test_continuous_vlm_chat():
        """Test continuous chat streaming with a VLM using runtime user input and images"""
        test_model = "granite3.2-vision:latest"  # Set to an appropriate VLM model available in your Ollama instance
        system_prompt = "You are a helpful vision assistant that can analyze images."
        
        # Get images directory from user
        default_images_dir = str(Path(__file__).parent)
        images_dir = input(f"\nEnter directory with images (default: {default_images_dir}): ") or default_images_dir
        
        print("\nContext Retention Options:")
        print("1. Full context retention (default)")
        print("2. Only retain user messages")
        print("3. Only retain assistant responses")
        print("4. No context retention (stateless)")
        
        try:
            choice = int(input("\nSelect an option (1-4): "))
            
            include_user = True
            include_assistant = True
            
            if choice == 2:
                include_assistant = False
            elif choice == 3:
                include_user = False
            elif choice == 4:
                include_user = False
                include_assistant = False
            
            # Check if user wants to use tools
            use_tools = input("\nDo you want to use vision tools? (y/n, default: n): ").lower().startswith('y')
            
            tools = None
            if use_tools:
                tools = [
                    get_weather_tool_definition(),
                    get_search_tool_definition(),
                    get_identify_object_tool_definition()
                ]
                print(f"Enabled {len(tools)} vision tools")
                
            # Call interactive VLM chat with selected options
            interactive_vlm_session(
                model=test_model,
                images_dir=images_dir,
                system_prompt=system_prompt,
                include_user_messages=include_user,
                include_assistant_responses=include_assistant,
                tools=tools
            )
        except ValueError:
            print("Invalid choice. Using default (full context retention).")
            interactive_vlm_session(
                model=test_model,
                images_dir=images_dir,
                system_prompt=system_prompt
            )
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Test function for multi-image VLM
    def test_multi_image_vlm():
        """Test the multi-image VLM functionality"""
        test_prompt = "Compare these images and describe the key differences between them."
        
        # Get list of test images from user (default to current directory)
        default_images_dir = str(Path(__file__).parent)
        images_dir = input(f"\nEnter directory with test images (default: {default_images_dir}): ") or default_images_dir
        
        # Let user select which images to use
        image_files = list(Path(images_dir).glob("*.jpg")) + list(Path(images_dir).glob("*.png"))
        if not image_files:
            print(f"No image files found in {images_dir}. Please add some .jpg or .png files.")
            return
            
        print("\nAvailable images:")
        for i, img in enumerate(image_files):
            print(f"{i+1}. {img.name}")
            
        # Get user selection
        try:
            selections = input("\nEnter image numbers to use (comma-separated, e.g. '1,3'): ")
            selected_indices = [int(idx.strip()) - 1 for idx in selections.split(",")]
            selected_images = [str(image_files[idx]) for idx in selected_indices if 0 <= idx < len(image_files)]
            
            if not selected_images:
                # If no valid selection, use first two images
                selected_images = [str(image_files[0])]
                if len(image_files) > 1:
                    selected_images.append(str(image_files[1]))
                print(f"Using default selection: {[Path(img).name for img in selected_images]}")
        except Exception as e:
            # On any error, use first two images
            selected_images = [str(image_files[0])]
            if len(image_files) > 1:
                selected_images.append(str(image_files[1]))
            print(f"Using default selection due to error: {[Path(img).name for img in selected_images]}")
        
        # Get model from user
        default_model = "granite3.2-vision:latest"
        model = input(f"\nEnter model name (default: {default_model}): ") or default_model
        
        # Custom prompt option
        custom_prompt = input(f"\nEnter custom prompt (default: '{test_prompt}'): ")
        if custom_prompt:
            test_prompt = custom_prompt
            
        # Custom system prompt option
        default_system = f"You are a detailed image analyzer that carefully examines multiple images in sequence."
        custom_system = input(f"\nEnter custom system prompt (default: '{default_system}'): ")
        system_prompt = custom_system if custom_system else default_system
        
        print(f"\nRunning multi-image VLM test with:")
        print(f"Model: {model}")
        print(f"Images: {[Path(img).name for img in selected_images]}")
        print(f"Prompt: {test_prompt}")
        print(f"System: {system_prompt}")
        
        # Use real-time streaming for the best user experience
        try:
            stream_vlm_multi_image(
                prompt=test_prompt,
                image_paths=selected_images,
                model=model,
                system=system_prompt
            )
        except Exception as e:
            print(f"\nError during multi-image VLM test: {str(e)}")
    
    # Test function for interactive multi-image VLM
    def test_interactive_multi_image_vlm():
        """Test the interactive multi-image VLM session functionality"""
        test_model = "granite3.2-vision:latest"  # Set to an appropriate VLM model available in Ollama
        
        # Get images directory from user
        default_images_dir = str(Path(__file__).parent)
        images_dir = input(f"\nEnter directory with images (default: {default_images_dir}): ") or default_images_dir
        
        print("\nContext Retention Options:")
        print("1. Full context retention (default)")
        print("2. Only retain user messages")
        print("3. Only retain assistant responses")
        print("4. No context retention (stateless)")
        
        try:
            choice = int(input("\nSelect an option (1-4): "))
            
            include_user = True
            include_assistant = True
            
            if choice == 2:
                include_assistant = False
            elif choice == 3:
                include_user = False
            elif choice == 4:
                include_user = False
                include_assistant = False
            
            # Check if user wants to use tools
            use_tools = input("\nDo you want to use vision tools? (y/n, default: n): ").lower().startswith('y')
            
            tools = None
            if use_tools:
                tools = [
                    get_weather_tool_definition(),
                    get_search_tool_definition(),
                    get_identify_object_tool_definition()
                ]
                print(f"Enabled {len(tools)} vision tools")
                
            # Custom system prompt option
            default_system = "You are a helpful vision assistant that can analyze multiple images in sequence."
            custom_system = input(f"\nEnter custom system prompt (default: '{default_system}'): ")
            system_prompt = custom_system if custom_system else default_system
            
            # Call interactive multi-image VLM chat with selected options
            interactive_multi_image_vlm_session(
                model=test_model,
                images_dir=images_dir,
                system_prompt=system_prompt,
                include_user_messages=include_user,
                include_assistant_responses=include_assistant,
                tools=tools
            )
        except ValueError:
            print("Invalid choice. Using default (full context retention).")
            interactive_multi_image_vlm_session(
                model=test_model,
                images_dir=images_dir
            )
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Test function for chronological image analysis
    def test_chronological_image_vlm():
        """Test the VLM with all images from a directory, sorted by timestamp or filename."""
        import os
        import re
        from datetime import datetime
        
        # Get images directory from user
        default_images_dir = str(Path(__file__).parent)
        images_dir = input(f"\nEnter directory with images (default: {default_images_dir}): ") or default_images_dir
        
        # Sorting option
        print("\nSort images by:")
        print("1. Modification timestamp (default)")
        print("2. Filename (alphabetical)")
        print("3. Filename with numerical pattern (e.g., img_001.jpg, img_002.jpg)")
        
        sort_choice = input("\nSelect sorting method (1-3): ") or "1"
        
        # Exclusion pattern
        exclusion_pattern = input("\nEnter pattern to exclude files (optional, e.g. 'thumb' or '.*.thumb.*'): ")
        
        # Find all image files in the directory
        image_files = []
        supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        
        for file in os.listdir(images_dir):
            file_path = os.path.join(images_dir, file)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file_path)
                if ext.lower() in supported_extensions:
                    # Skip if it matches exclusion pattern
                    if exclusion_pattern and re.search(exclusion_pattern, file_path):
                        print(f"Excluding: {file}")
                        continue
                        
                    # Store relevant sorting key based on user choice
                    if sort_choice == "1":  # Sort by timestamp
                        sort_key = os.path.getmtime(file_path)
                        display_info = ("timestamp", sort_key)
                    elif sort_choice == "2":  # Sort by filename (alphabetical)
                        sort_key = file.lower()  # Case-insensitive sort
                        display_info = ("filename", file)
                    elif sort_choice == "3":  # Sort by numeric pattern in filename
                        # Try to extract numbers from the filename for natural sorting
                        numbers = re.findall(r'\d+', file)
                        # If numbers found, use the last number group for sorting
                        if numbers:
                            # Create a sortable key by padding the number with zeros
                            numeric_part = numbers[-1]
                            sort_key = file.replace(numeric_part, numeric_part.zfill(10))
                        else:
                            # If no numbers, just use the filename
                            sort_key = file.lower()
                        display_info = ("numeric pattern", file)
                    else:
                        sort_key = os.path.getmtime(file_path)  # Default to timestamp
                        display_info = ("timestamp", sort_key)
                    
                    image_files.append((file_path, sort_key, display_info))
        
        # Sort images by the chosen method
        image_files.sort(key=lambda x: x[1])  # type: ignore # Sort by the sort_key (second element of tuple)
        
        # Convert to list of just paths
        sorted_image_paths = [img[0] for img in image_files] # type: ignore
        
        if not sorted_image_paths:
            print(f"No image files found in {images_dir}. Please add some images and try again.")
            return
        
        # Print the sorted images with sorting information
        sort_method = "timestamp" if sort_choice == "1" else "filename" if sort_choice == "2" else "numeric pattern"
        print(f"\nImages sorted by {sort_method} (ascending order):")
        for i, (img_path, _, display_info) in enumerate(image_files):
            method, value = display_info
            if method == "timestamp":
                # Convert timestamp to readable date
                info = datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
            else:
                info = value
            print(f"{i+1}. {os.path.basename(img_path)} - {info}")
        
        # Ask if user wants to proceed with this order
        proceed = input("\nProceed with this order? (y/n, default: y): ").lower() != 'n'
        if not proceed:
            print("Operation cancelled by user.")
            return
            
        # Ask if the user wants to reverse the order
        reverse_order = input("\nReverse the order (newest/last first)? (y/n, default: n): ").lower() == 'y'
        if reverse_order:
            sorted_image_paths.reverse()
            print("Order reversed.")
        
        # Get model from user
        default_model = "granite3.2-vision:latest"
        model = input(f"\nEnter model name (default: {default_model}): ") or default_model
        
        # Get prompt from user
        chronological_terms = "chronologically" if sort_choice == "1" else "sequentially"
        default_prompt = f"Analyze these images that are sorted {chronological_terms}. Describe what you see and any changes or progression across the sequence."
        custom_prompt = input(f"\nEnter custom prompt (default: '{default_prompt}'): ")
        prompt = custom_prompt if custom_prompt else default_prompt
        
        # Create a specialized system prompt based on sorting method
        if sort_choice == "1":  # Timestamp
            order_description = "CHRONOLOGICAL ORDER (sorted by timestamp from oldest to newest)"
            if reverse_order:
                order_description = "REVERSE CHRONOLOGICAL ORDER (sorted by timestamp from newest to oldest)"
        else:  # Filename-based
            order_description = "SEQUENTIAL ORDER (sorted by filename)"
            if reverse_order:
                order_description = "REVERSE SEQUENTIAL ORDER (sorted by filename in reverse)"
        
        default_system = f"""You are an advanced vision assistant analyzing a sequence of {len(sorted_image_paths)} images.
IMPORTANT: These images are provided in {order_description}.
When referring to the images, use 'first image', 'second image', etc. through to 'image {len(sorted_image_paths)}'.
Analyze both individual images and the progression/changes across the sequence.
If timestamps or sequence indicators are visible in the images, note them and use them to enhance your analysis.
"""
        
        custom_system = input(f"\nEnter custom system prompt (or press Enter for default): ")
        system_prompt = custom_system if custom_system else default_system
        
        print(f"\nRunning sequential image analysis with:")
        print(f"Model: {model}")
        print(f"Number of images: {len(sorted_image_paths)}")
        print(f"Prompt: {prompt}")
        print(f"System: {system_prompt[:100]}..." if len(system_prompt) > 100 else f"System: {system_prompt}")
        
        # Determine whether to use streaming based on user preference
        use_streaming = input("\nUse streaming mode? (y/n, default: y): ").lower() != 'n'
        
        try:
            if use_streaming:
                # Use real-time streaming for better user experience
                stream_vlm_multi_image(
                    prompt=prompt,
                    image_paths=sorted_image_paths,
                    model=model,
                    system=system_prompt,
                    sequence_aware_system=True  # Ensure sequence awareness is enabled
                )
            else:
                # Use non-streaming version
                response = vlm_generate_multi_image(
                    prompt=prompt,
                    image_paths=sorted_image_paths,
                    model=model,
                    system=system_prompt,
                    sequence_aware_system=True  # Ensure sequence awareness is enabled
                )
                
                # Display the response
                print("\nVLM Response:")
                print("-" * 50)
                print(response.get("response", "No response found"))
                print("-" * 50)
        except Exception as e:
            print(f"\nError during sequential image analysis: {str(e)}")
    
    def get_screenshot_events_from_json():
        """Get screenshot events from a JSON file"""
        json_file_path = os.path.join(workspace_data_dir,
                                    'youtube.com/123e4567-e89b-12d3-a456-426614174000/screenshot_events_123e4567-e89b-12d3-a456-426614174000.json'
                                                                        )
        logger.info(f"Loading screenshot events from JSON file: {json_file_path}")
            
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"JSON file not found: {json_file_path}")
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                events_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file: {str(e)}")
        
        if not events_data or not isinstance(events_data, list):
            raise ValueError("JSON file does not contain a list of screenshot events")
        
        # Convert JSON data to ScreenshotEvent objects
        screenshot_events = []
        for event_dict in events_data:
            # Convert ISO format string back to datetime
            if 'timestamp' in event_dict:
                event_dict['timestamp'] = datetime.fromisoformat(event_dict['timestamp']) # type: ignore
            
            screenshot_path = event_dict["screenshot_path"] # type: ignore
            # convert screenshot_path to proper path using paths config
            screenshot_path = workspace_dir / screenshot_path
            event_dict["screenshot_path"] = str(screenshot_path) # type: ignore
            # Create ScreenshotEvent object
            try:
                event = ScreenshotEvent(**event_dict)
                screenshot_events.append(event)
            except (TypeError, ValueError) as e:
                logger.warning(f"Skipping invalid event: {str(e)}")
        
        logger.info(f"Loaded {len(screenshot_events)} screenshot events from JSON file")
        return screenshot_events
    
    def test_screenshot_events_analysis():
        # Test the non-streaming function
        print("\nTesting screenshot events analysis with VLM...")
        screenshot_events = get_screenshot_events_from_json()
        
        # Check if screenshot files actually exist
        for i, event in enumerate(screenshot_events):
            path = event.screenshot_path
            exists = os.path.exists(path)
            print(f"Screenshot {i+1} path: {path}")
            print(f"File exists: {exists}")
            
            # If file doesn't exist, try to find it in a different location
            if not exists:
                print(f"Warning: Screenshot file doesn't exist at {path}")
                
                # Try different path variations
                alt_path = Path(workspace_dir) / "data" / path.name
                if os.path.exists(alt_path):
                    print(f"Found at alternative path: {alt_path}")
                    event.screenshot_path = alt_path
        
        # this function should stream the vlm analysis of the screenshot events
        #  and also save the response to a string and print it after the stream is complete
        response = stream_vlm_analyze_screenshot_events(
            screenshot_events=screenshot_events,
            user_prompt="Where should I click to search on the given website screenshot?",
            model="granite3.2-vision:latest",
            # system_prompt="You are a helpful vision assistant that can analyze multiple images in sequence."
        )
        print("\nVLM Analysis Response:")
        print(response)
            
            

    # Run the test functions
    if __name__ == "__main__":
        
        # LLM tests
        #test_regular_generation()
        #test_streaming_generation()
        #test_real_time_streaming(use_system_prompt=True)
        # test_continuous_chat_streaming()
        
        # VLM tests
        #test_regular_vlm_generation()
        #test_streaming_vlm_generation()
        #test_real_time_vlm_streaming()
        #test_continuous_vlm_chat()  # Run the VLM continuous chat test
        #test_multi_image_vlm()  # Run the multi-image VLM test
        #test_interactive_multi_image_vlm()  # Run the interactive multi-image VLM test
        # test_chronological_image_vlm()  # Run the chronological image analysis test
        test_screenshot_events_analysis() 