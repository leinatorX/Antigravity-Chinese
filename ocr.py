import sys
import Quartz
import Vision
from Cocoa import NSURL

def recognize_text(image_path):
    url = NSURL.fileURLWithPath_(image_path)
    handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    
    results = []
    def completion_handler(request, error):
        if error:
            print("Error:", error)
            return
        for observation in request.results():
            top_candidate = observation.topCandidates_(1).firstObject()
            if top_candidate:
                results.append(top_candidate.string())
                
    request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(completion_handler)
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    
    handler.performRequests_error_([request], None)
    return "\n".join(results)

if __name__ == "__main__":
    import glob
    # Find the latest media file
    files = glob.glob("/Users/yuhonglei/.gemini/antigravity/brain/470eb003-fe56-4c38-bfbd-d865b27bdf45/media_*.png")
    if not files:
        print("No image found.")
    else:
        latest_file = max(files, key=lambda f: f.split("media__")[1].split(".")[0])
        print("Extracting from:", latest_file)
        text = recognize_text(latest_file)
        print("--- EXTRACTED TEXT ---")
        print(text)
        print("--- HEX DUMP OF EXTRACTED TEXT ---")
        import binascii
        print(binascii.hexlify(text.encode('utf-8')))
