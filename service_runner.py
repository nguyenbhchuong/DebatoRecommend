from taggingService.tag_service import TaggingService

def main():
    service = TaggingService()
    try:
        print("Starting tagging service...")
        service.start(timeout=None)
    except KeyboardInterrupt:
        print("Shutting down tagging service...")

if __name__ == "__main__":
    main() 