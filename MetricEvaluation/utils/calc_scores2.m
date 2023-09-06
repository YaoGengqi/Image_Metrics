function scores = calc_scores(input_dir,GT_dir,shave_width,verbose)

addpath(genpath(fullfile(pwd,'utils')));

%% Loading model
load modelparameters.mat
blocksizerow    = 96;
blocksizecol    = 96;
blockrowoverlap = 0;
blockcoloverlap = 0;

% Only read the img exists in GTROOT-Folder.
file_list = dir([GT_dir,'/*.png']); % use the GTFile list to list the SR_list.
GT_list = dir([GT_dir,  '/*.png']);

dat = {GT_list.name};
im_num = length(GT_list);

scale = 4;
scores = struct([]);

filterName = {'ImgName\Metrics','PSNR','SSIM','PI','BIQME','FADE','AG','IE','Var','MSE','RMSE','Ma','NIQE','LPIPS','FID'};
xlswrite([input_dir '\ALlMetrics.xlsx'], filterName(:)', 'A1:O1');
xlswrite([input_dir '\ALlMetrics.xlsx'], dat(:), ['A2:A' num2str(im_num+1)]);

metricData = zeros(im_num,14);   % initiate all metrics data to be 0.
k = 0;

for ii=1:im_num

    if verbose
        fprintf(['> Calculating scores for image ',num2str(ii),' / ',num2str(im_num), '...\n']);
    end
    
    % Reading and converting images
    input_image_path = fullfile(input_dir,file_list(ii).name);
    input_image = convert_shave_image(imread(input_image_path),shave_width);

    GD_image_path = fullfile(GT_dir,GT_list(ii).name);
    GD_image = modcrop(imread(GD_image_path), scale);
    GD_image = convert_shave_image(GD_image,shave_width);   % 转化为单通道！

    if size(input_image) ~= size(GD_image)
        display("The size is different between the SR_image and GT_image! ")
        display(size(input_image), input_image_path)
        display(size(GD_image), GD_image_path)
    end

    % Calculating scores
    scores(ii).name     = file_list(ii).name;
    % scores(ii).MSE      = immse(input_image,GD_image);
    scores(ii).MSE      = 0;
    scores(ii).Ma       = quality_predict(input_image);
    scores(ii).PSNR     = psnr(input_image, GD_image);
    [scores(ii).SSIM,scores(ii).SSIM_map] = ssim(input_image, GD_image);
    scores(ii).NIQE     = computequality(input_image,blocksizerow,blocksizecol,...
                                         blockrowoverlap,blockcoloverlap,mu_prisparam,cov_prisparam);


    img = imread(input_image_path); % 不转换为单通道

    if length(size(img)) == 2
        [m,n] = size(img);
        A = zeros(m,n,3);
        for x = 1:3
            A(:,:,x) = img;
        end
        img = A;
    end

    % scores(ii).BIQME    = BIQME(img);
    % scores(ii).FADE     = FADE(img);
    % scores(ii).AG       = AG(img);
    % scores(ii).IE       = IE(img);
    % scores(ii).VAR      = Var(img);

    scores(ii).BIQME    = 0;
    scores(ii).FADE     = 0;
    scores(ii).AG       = 0;
    scores(ii).IE       = 0;
    scores(ii).VAR      = 0;

    k = k + 1;

    % filterName = {'ImgName','PSNR','SSIM','PI','BIQME','FADE','AG','IE','Var','MSE','RMSE','Ma','NIQE','LPIPS'};

    metricData(k,1)  = scores(ii).PSNR;
    metricData(k,2)  = scores(ii).SSIM;
    metricData(k,3)  = ((scores(ii).NIQE +(10 - scores(ii).Ma))/2);
    metricData(k,4)  = scores(ii).BIQME;
    metricData(k,5)  = scores(ii).FADE;
    metricData(k,6)  = scores(ii).AG;
    metricData(k,7)  = scores(ii).IE;
    metricData(k,8)  = scores(ii).VAR;
    metricData(k,9)  = scores(ii).MSE;
    metricData(k,10) = sqrt(scores(ii).MSE);
    metricData(k,11) = scores(ii).Ma;
    metricData(k,12) = scores(ii).NIQE;

end

xlswrite([input_dir '\ALlMetrics.xlsx'], metricData, ['B2:O' num2str(im_num+1) ]);
means = {'Average', num2str(mean([scores.PSNR])), num2str(mean([scores.SSIM])), num2str((mean([scores.NIQE]) + (10 - mean([scores.Ma]))) / 2), num2str(mean([scores.BIQME])), num2str(mean([scores.FADE])), num2str(mean([scores.AG])), num2str(mean([scores.IE])), num2str(mean([scores.VAR])), num2str(mean([scores.MSE])), num2str(sqrt(mean([scores.MSE]))), num2str(mean([scores.Ma])), num2str(mean([scores.NIQE])), "0", "0"};
xlswrite([input_dir '\ALlMetrics.xlsx'], means, ['A' num2str(im_num+2) ':O' num2str(im_num+2)]);

end

function img = modcrop(img, modulo)
if size(img,3) == 1
    sz = size(img);
    sz = sz - mod(sz, modulo);
    img = img(1:sz(1), 1:sz(2));
else
    tmpsz = size(img);
    sz = tmpsz(1:2);
    sz = sz - mod(sz, modulo);
    img = img(1:sz(1), 1:sz(2),:);
end
end
