close all; clc; 
clear;
%% Get data
% datafile = uigetfile('D:\Drive\desktop\research\shape_tracking\data\automated\*.mat')
load('-mat',uigetfile)
data = normalize(data);
mag_train = data(:,1:3);
servo_train = data(:,4:5);
%%
train_data = extract_endpoints(cam1_frames,data);


%%
data_servo_1 =    [servo_train, train_data(:,6)];
data_servo_2 =    [servo_train, train_data(:,7)];
data_mag_1 =      [mag_train, train_data(:,6)];
data_mag_2 =      [mag_train, train_data(:,7)];
data_combined_1 = [data, train_data(:,6)];
data_combined_2 = [data, train_data(:,7)];
%% Train models
[servo_1_model, servo_1_rmse] = trainServoGPR(data_servo_1);
[servo_2_model, servo_2_rmse] = trainServoGPR(data_servo_2);
[mag_1_model, mag_1_rmse] = trainMagGPR(data_mag_1);
[mag_2_model, mag_2_rmse] = trainMagGPR(data_mag_2);
[combined_1_model, combined_1_rmse] = trainCombinedGPR(data_combined_1);
[combined_2_model, combined_2_rmse] = trainCombinedGPR(data_combined_2);

%% Get Test data
load('-mat',uigetfile)
data = normalize(data);
%%
test_data = extract_endpoints(cam1_frames,data);
mag_test = data(:,1:3);
servo_test = data(:,4:5);
y_test = test_data(:,6:7);
%%
disp("Servo 1:")
[bias_servo_1,std_servo_1,y_hat_servo_1] = predict(servo_1_model,servo_test,y_test(:,1));
disp("Servo 2:")
[bias_servo_2,std_servo_2,y_hat_servo_2] = predict(servo_2_model,servo_test,y_test(:,2));
disp("Mag 1:")
[bias_mag_1,std_mag_1,y_hat_mag_1] = predict(mag_1_model,mag_test,y_test(:,1));
disp("Mag 2:")
[bias_mag_2,std_mag_2,y_hat_mag_2] = predict(mag_2_model,mag_test,y_test(:,2));
disp("Combined 1:")
[bias_comb_1,std_comb_1,y_hat_comb_1] = predict(combined_1_model,[mag_test,servo_test],y_test(:,1));
disp("Combined 2:")
[bias_comb_2,std_comb_2,y_hat_comb_2] = predict(combined_2_model,[mag_test,servo_test],y_test(:,2));

%%
function [new_data] = extract_endpoints(cam1_frames,data)
[posN,~,~] = size(cam1_frames);
cam1_data = struct();
cam1_data.Centroids = zeros(posN,2);
cam1_data.Theta = zeros(posN,1);
cam1_data.Length = zeros(posN,1);
cam1_data.Endpoint = zeros(posN,2);

threshold = 1.5;
figure
for i = 1:posN
    frame1 = get_frame(cam1_frames,i);
    imshow(frame1);
    [mframe1,processed1] = maskout(frame1,threshold);
    
    stats1 = regionprops(processed1,'Area','Centroid','MajorAxisLength','Orientation');
    [num_regions,~] = size(stats1);
    if num_regions > 1
        pause()
    end
    cam1_data.Centroids(i,:) = stats1.Centroid;
    cam1_data.Theta(i,:) = (90+stats1.Orientation)*pi/180;
    cam1_data.Length(i,:) = stats1.MajorAxisLength;


    l = cam1_data.Length(i,:);
    x = cam1_data.Centroids(i,1);
    y = cam1_data.Centroids(i,2);
    o = cam1_data.Theta(i,:);
  
    q1 = [x+0.5*l*sin(o), y+0.5*l*cos(o)];
    q2 = [x-0.5*l*sin(o), y-0.5*l*cos(o)];
    ends = [q1;q2];
    screen_center = [320,240];
    distal_distances = pdist2(screen_center,ends);
    [~, max_idx] = max(distal_distances);
    max_end = ends(max_idx,:);
    cam1_data.Endpoint(i,:) = max_end;
    
%     imshow(mframe1*1.5)
%     hold on
%     scatter(max_end(1),max_end(2),100,'filled','g');
    
    %line([x, ],[y, ])
    %line([x, ], [y, ])
    %rectangle('Position',cam1_data.BBox(i,:),'EdgeColor','w')
%    
    pause();


end
[dataN,~] = size(data);
Endpoint = zeros(dataN,2);
nsamples = round(dataN/posN);

for i  = 1:posN
%     Theta(1+(i-1)*nsamples:i*nsamples) = repmat(cam1_data.Theta(i),nsamples,1);
%     Length(1+(i-1)*nsamples:i*nsamples) = repmat(cam1_data.Length(i),nsamples,1);
    Endpoint(1+(i-1)*nsamples:i*nsamples,:)  = repmat(cam1_data.Endpoint(i,:),nsamples,1);
end
Endpoint = Endpoint*25/40;
new_data = [data, Endpoint];
end
%%

function data = normalize(data)
    neutral_y1 = data(:,4)== 512;
    data_ny1 = data(neutral_y1,:);
    neutral_y2 = data_ny1(:,5) == 512;
    data_neutral = data_ny1(neutral_y2,:);
    neutral_mean = mean(data_neutral);
    neutral_x = neutral_mean(1:3);
    data = [data(:,1:end-2)-neutral_x, data(:,end-1:end)];
end
function frame = get_frame(cam_frames, idx)
raw = squeeze(cam_frames(idx,:,:,:));
normalized = raw/255;
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