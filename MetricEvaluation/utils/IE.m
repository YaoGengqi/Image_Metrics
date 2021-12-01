function [ imgIE ] = IE(inputImg)
image = inputImg;

if numel(size(image)) > 2
    img=rgb2gray(image);
end

[m,n]=size(img);
    
imax=ceil(max(max(img)))+1;
temp=zeros(1,imax);
% ��ͼ��ĻҶ�ֵ��[0,imax]����ͳ��
for i=1:m;
    for j=1:n;
        if (img(i,j)==imax)
            x=imax+1;
        else
            x=fix(img(i,j))+1;
        end
        temp(x)=temp(x)+1;
    end
end
temp=temp./(m*n);
%���صĶ���������
imgIE=0;
for i=1:length(temp)
    if (temp(i)==0)
        imgIE = imgIE;
    else
        imgIE = imgIE-temp(i)*log2(temp(i));
    end
end

end
