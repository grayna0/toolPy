
import requests



# Gửi yêu cầu HTTP để lấy thông tin video
def getSub(api_url,video_id):
    print(api_url,video_id)
    # Thiết lập các tiêu đề HTTP
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': f'{video_id}',
        'Cookie': 'your_cookie_here'  # Thay thế bằng cookie thực tế của bạn nếu cần
    }
    response = requests.get(api_url, headers=headers)
    ojbSub= []
    if response.status_code == 200:
        video_info = response.json()
        ojbSub = video_info['body']
    listSub= "" 
    for contents in ojbSub:
            listSub = f"{listSub} /n {contents['content']}"
    with open("C:/Users/pc/myPyPro/result/listSub.txt", 'a+',encoding='utf-8') as file:
         file.write(listSub)
    return listSub  
         

         
