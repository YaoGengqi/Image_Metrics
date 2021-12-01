function [ imgVar ] = Var(inputImg)
image1 = inputImg;
image = im2double(image1);
img = rgb2gray(image);
[m,n]=size(img);
    
k=(sum(sum(img)))/(m*n);
gray_ave=0;
for i=1:m
    gray_ave1=0;
    for j=1:n
       gray_ave1=gray_ave1+(img(i,j)-k)*(img(i,j)-k);
    end
    gray_ave=gray_ave+gray_ave1;
end
    gray_ave=255*gray_ave/(m*n);
imgVar = gray_ave;
end
