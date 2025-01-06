
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
            listSub = f"{listSub} \n {contents['content']}"
    with open("C:/Users/pc/toolPy/result/listSub.txt", 'a',encoding='utf-8') as file:
         file.write(listSub)
    return listSub  
getSub(api_url="https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/1136056766995172720989332742d457eb452b83b475056ae2974d8c79?auth_key=1736150676-88a6bf701d354c848d0178651013d2cb-0-485566df72f204cb9fb0934ab51cedba",video_id="https://www.bilibili.com/video/BV1xMiBYUEBM/?spm_id_from=333.337.search-card.all.click&vd_source=1124f7b904b73e398c740b637205feb4")
         

         
