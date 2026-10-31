from PIL import Image, ImageDraw, ImageFont
S=512
img=Image.new("RGBA",(S,S),(0,0,0,0))
d=ImageDraw.Draw(img)
# rounded square base with subtle vertical gradient
for y in range(S):
    t=y/S
    r=int(10+10*t); g=int(11+13*t); b=int(14+18*t)
    d.line([(0,y),(S,y)],fill=(r,g,b,255))
mask=Image.new("L",(S,S),0)
ImageDraw.Draw(mask).rounded_rectangle([0,0,S-1,S-1],radius=118,fill=255)
img.putalpha(mask)
d=ImageDraw.Draw(img)
# acid arc ring (sun path)
cx,cy,R=256,262,132
d.arc([cx-R,cy-R,cx+R,cy+R],start=-95,end=200,fill=(198,255,61,255),width=20)
# horizon line
d.line([(cx-R-22,cy+R+30),(cx+R+22,cy+R+30)],fill=(255,255,255,60),width=8)
# center dot
d.ellipse([cx-26,cy-26,cx+26,cy+26],fill=(198,255,61,255))
img.convert("RGB").save("/root/lifeapp/icon512.png")
for size,name in [(48,'mdpi'),(72,'hdpi'),(96,'xhdpi'),(144,'xxhdpi'),(192,'xxxhdpi')]:
    img.resize((size,size),Image.LANCZOS).convert("RGB").save(f"/root/lifeapp/res/mipmap-{name}/ic_launcher.png")
print("ok")
