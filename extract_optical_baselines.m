close all; clc;
%clear;
% %% Get data
% datafile = uigetfile('D:\Drive\desktop\research\shape_tracking\data\automated\*.mat')
% importfile(datafile);
% N = length(data);
% Xs = data(:,1:3);
% ys = data(:,4:5);
%%
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

for i = 1:N
    frame1 = get_frame(cam1_frames,i);
    frame2 = get_frame(cam2_frames,i);
    
    processed1 = maskout(frame1,threshold);
    processed2 = maskout(frame2,threshold);
    
    stats1 = regionprops(processed1,'Area','Centroid','MajorAxisLength','Orientation');
    stats2 = regionprops(processed2,'Area','Centroid','MajorAxisLength','Orientation');
    [num_regions,~] = size(stats1);
    if num_regions > 1
        pause()
    end
    cam1_data.Centroids(i,:) = stats1.Centroid;
    %cam1_data.BBox(i,:) = stats1.BoundingBox;
    cam1_data.Theta(i,:) = stats1.Orientation;
    cam1_data.Length(i,:) = stats1.MajorAxisLength;
    
    cam2_data.Centroids(i,:) = stats2.Centroid;
    %cam2_data.BBox(i,:) = stats2.BoundingBox;
    cam2_data.Theta(i,:) = stats2.Orientation;
    cam2_data.Length(i,:) = stats2.MajorAxisLength;


    imshow(processed1);
    hold on
    line([0 cam1_data.Centroids(i,1)],[0 cam1_data.Centroids(i,2)])
%     
    pause(0.07);


end
%%
function frame = get_frame(cam_frames, idx)
raw = squeeze(cam_frames(idx,:,:,:));
normalized = raw/25;
frame = flip(normalized,3);

end
function masked = maskout(src,threshold)
    % mask: binary, same size as src, but does not have to be same data type (int vs logical)
    % src: rgb or gray image
    red_chan = src(:,:,1);
    cyan_chan = 0.5*(src(:,:,2)+src(:,:,3));
    masked = red_chan./cyan_chan >  threshold;
    SE = strel('disk',10,4);
    cleaned = imopen(masked,SE);
    masked = imclose(cleaned,SE);
    %masked = bsxfun(@times, src, cast(mask,class(src)));
end