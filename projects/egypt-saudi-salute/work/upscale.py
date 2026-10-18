import cv2, numpy as np, sys
sr=cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel('work/EDSR_x2.pb'); sr.setModel('edsr',2)
im=cv2.imread('assets/photo.png'); H,W=im.shape[:2]; T=256; P=12
out=np.zeros((H*2,W*2,3),np.uint8)
for y in range(0,H,T):
    for x in range(0,W,T):
        y0,x0=max(0,y-P),max(0,x-P); y1,x1=min(H,y+T+P),min(W,x+T+P)
        u=sr.upsample(im[y0:y1,x0:x1])
        oy,ox=(y-y0)*2,(x-x0)*2; h,w=min(T,H-y)*2,min(T,W-x)*2
        out[y*2:y*2+h,x*2:x*2+w]=u[oy:oy+h,ox:ox+w]
    print('row',y,flush=True)
cv2.imwrite('assets/photo@2x.jpg',out,[cv2.IMWRITE_JPEG_QUALITY,94]); print('DONE',out.shape)
