function [ AVEGRAD ] = AG(inputImg)
image1 = inputImg;
image=im2double(image1);
img=rgb2gray(image);
[m,n]=size(img);
    
gradval=zeros(m,n); %%% save the gradient value of single pixel
diffX=zeros(m,n); %%% save the differential value of X orient
diffY=zeros(m,n); %%% save the differential value of Y orient
tempX=zeros(m,n);
tempY=zeros(m,n);
tempX(1:m,1:(n-1))=img(1:m,2:n);
tempY(1:(m-1),1:n)=img(2:m,1:n);
diffX=tempX-img;
diffY=tempY-img;
diffX(1:m,n)=0; %%% the boundery set to 0
diffY(m,1:n)=0;
diffX=diffX.*diffX;
diffY=diffY.*diffY;
AVEGRAD=(diffX+diffY)/2;
AVEGRAD=sum(sum(sqrt(AVEGRAD)));
AVEGRAD=AVEGRAD/((m-1)*(n-1));
AVEGRAD=AVEGRAD*255;

end

