from translate import Translator
import functions.Get_Sub_bilibili 
translator= Translator(from_lang="zh-chi",to_lang="vi")
subVit=[]
for sub in functions.Get_Sub_bilibili.slice_object:
    
    
    translation = translator.translate(sub)
    subVit.append(translation)
    
print(subVit)