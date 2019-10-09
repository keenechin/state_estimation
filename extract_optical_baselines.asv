close all; clc;
%clear;
% %% Get data
% datafile = uigetfile('D:\Drive\desktop\research\shape_tracking\data\automated\*.mat')
load('-mat',uigetfile)
% N = length(data);
% Xs = data(:,1:3);
% ys = data(:,4:5);
%%
close all
[N,X,Y] = size(cam1_frames);
cam1_data = struct();
cam1_data.Centroids = zeros(N,2);
%cam1_data.BBox = zeros(N,4);
cam1_data.Theta = zeros(N,1);
cam1_data.Length = zeros(N,1);
cam2_data.Centroids = zeros(N,2);
%cam2_data.BBox = zeros(N,4);
cam2_data.Theta = zeros(N,1);
cam2_data.Length = zeros(N,1);

threshold = 1.8;

for i = 1:N-1
    frame1 = get_frame(cam1_frames,i+1);
    frame2 = get_frame(cam2_frames,i+1);
    
    [mframe1,processed1] = maskout(frame1,threshold);
    [mframe2,processed2] = maskout(frame2,threshold);
    
    stats1 = regionprops(processed1,'Area','Centroid','MajorAxisLength','Orientation','BoundingBox');
    stats2 = regionprops(processed2,'Area','Centroid','MajorAxisLength','Orientation','BoundingBox');
    [num_regions,~] = size(stats1);
    if num_regions > 1
        pause()
    end
    cam1_data.Centroids(i,:) = stats1.Centroid;
    cam1_data.BBox(i,:) = stats1.BoundingBox;
    cam1_data.Theta(i,:) = (90+stats1.Orientation)*pi/180;
    cam1_data.Length(i,:) = stats1.MajorAxisLength;
    
    cam1_data.Centroids(i,:) = stats1.Centroid;
    cam1_data.BBox(i,:) = stats1.BoundingBox;
    cam1_data.Theta(i,:) = (90+stats1.Orientation)*pi/180;
    cam1_data.Length(i,:) = stats1.MajorAxisLength;


    l = cam1_data.Length(i,:);
    x = cam1_data.Centroids(i,1);
    y = cam1_data.Centroids(i,2);
    o = cam1_data.Theta(i,:);
    imshow(mframe1);
    hold on
    scatter(x,y,20,'filled','b')
    line([x, x+0.5*l*sin(o)],[y, y+0.5*l*cos(o)])
    line([x, x-0.5*l*sin(o)], [y, y-0.5*l*cos(o)])
    %rectangle('Position',cam1_data.BBox(i,:),'EdgeColor','w')
%     
    pause(0.07);


end
%%
old_data = data;
[length,~] = size(data);
cam1_data.Theta(end) = cam1_data.Theta(end-1)+(cam1_data.Theta(end-1)-cam1_data.Theta(end-2))
Theta = zeros(length,1);
nsamples = round(length/N);

for i  = 1:N
    Theta(1+(i-1)*nsamples:i*nsamples) = repmat(cam1_data.Theta(i),nsamples,1);
end
data = [data, Theta]
%%

train_portion = 0.8;
neutral_y1 = data(:,4)== 512;
data_ny1 = data(neutral_y1,:);
neutral_y2 = data_ny1(:,5) == 512;
data_neutral = data_ny1(neutral_y2,:);
neutral_mean = mean(data_neutral);
neutral_x = neutral_mean(1:3);
old_data = data;
data = [data(:,1:end-2)-neutral_x, data(:,end-1:end)];
    
%% Pre-process data set
[dataN,~] = size(data)
shuffled = data(randperm(dataN),:);
train_test_cutoff = floor(dataN*train_portion);
train_data = shuffled(1:train_test_cutoff-1,:);
test_data = shuffled(train_test_cutoff:end,:);
%%
y_train = train_data(:,end-1:end);
y_test = test_data(:,end-1:end);
X_train = train_data(:,1:end-2);
X_test = test_data(:,1:end-2);

%% Non-coupled pre-processing
[~,nfields] = size(data);
data_1 = data(data(:,end)==512,[1:nfields-2,nfields-1]);
data_2 = data(data(:,end-1)==512,[1:nfields-2,nfields]);
N1 = length(data_1);
N2 = length(data_2);
shuffled_1 = data_1(randperm(N1),:);
train_test_cutoff = floor(N1*train_portion);
train_data_1 = shuffled_1(1:train_test_cutoff-1,:);
test_data_1 = shuffled_1(train_test_cutoff:end,:);
shuffled_2 = data_2(randperm(N2),:);
train_test_cutoff = floor(N2*train_portion);
train_data_2 = shuffled_2(1:train_test_cutoff-1,:);
test_data_2 = shuffled_2(train_test_cutoff:end,:);
y_train_1 = train_data_1(:,end);
y_test_1 = test_data_1(:,end);
X_train_1 = train_data_1(:,1:end-1);
X_test_1 = test_data_1(:,1:end-1);
y_train_2 = train_data_2(:,end);
y_test_2 = test_data_2(:,end);
X_train_2 = train_data_2(:,1:end-1);
X_test_2 = test_data_2(:,1:end-1);


%% Train models
disp('training mimo1')
[regressor_mimo1, valid_rmse_mimo1] = trainUnivariateRegressionModel([X_train,y_train(:,1)]);%Regenerate these functions using the learner apps, whenever making changes to code
disp('training mimo2')
[regressor_mimo2, valid_rmse_mimo2] = trainUnivariateRegressionModel([X_train,y_train(:,2)]);%Regenerate these functions using the learner apps, whenever making changes to code

%% MIMO1
disp("MIMO 1:");
[bias_mimo1,std_mimo1,y_hat_mimo1] = predict(regressor_mimo1,X_test,y_test(:,1));
%title("Univariate model: Multimodal axis 1 > Multimodal axis 1")
%% MIMO2
disp("MIMO 2:");
[bias_mimo2,std_mimo2,y_hat_mimo2] = predict(regressor_mimo2,X_test,y_test(:,2));
%title("Univariate model: Multimodal axis 2 > Multimodal axis 2")
%%
% figure
% scatter(cam1_data.Centroids(1:end,1),cam1_data.Centroids(1:end,2))
% hold on
% center = mean(cam1_data.Centroids)
% scatter(center(1),center(2),20,'filled','r')
% figure
% scatter(cam1_data.Centroids(:,1)-center(1),cam1_data.Centroids(:,2)-center(2))
% 
% angles = atan2(cam1_data.Centroids(:,1),cam1_data.Centroids(:,2))

%%
function frame = get_frame(cam_frames, idx)
raw = squeeze(cam_frames(idx,:,:,:));
normalized = raw/25;
frame = flip(normalized,3);

end
function [masked, bw] = maskout(src,threshold)
    % mask: binary, same size as src, but does not have to be same data type (int vs logical)
    % src: rgb or gray image
    red_chan = src(:,:,1);
    cyan_chan = 0.5*(src(:,:,2)+src(:,:,3));
    mask = red_chan./cyan_chan >  threshold;
    SE = strel('disk',10,4);
    cleaned = imopen(mask,SE);
    bw = imclose(cleaned,SE);
    masked = bsxfun(@times, src, cast(bw,class(src)));
end