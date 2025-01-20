import json
# Read original JSON
def write_json_sub():
    with open("C:/Users/pc/toolPy/functions/subtitles.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Read Vietnamese translations
    with open("C:/Users/pc/toolPy/result/vietSub.txt", 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    # Update content for each subtitle entry
     # Replace content in each subtitle entry with Vietnamese lines
        for index, subtitle in enumerate(data["body"]):
            if index < len(lines):
                subtitle["content"] = lines[index]
    with open("C:/Users/pc/toolPy/functions/subtitlesViet.json", 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)        


   
