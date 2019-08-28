close all
clear
clc
%%
train_portion = 0.8;
%% Get data
importfile(uigetfile);
N = length(data);
Xs = data(:,1:3);
ys = data(:,4:5);
%%
pos_list = unique(data(:,4));
for i = 1: length(pos_list)
    pos = pos_list(i)
    %disp(std(data(data(:,4)==pos,:)))
end

%% Process whole data set
shuffled = data(randperm(N),:);
train_test_cutoff = floor(N*train_portion);
train_data = shuffled(1:train_test_cutoff-1,:);
test_data = shuffled(train_test_cutoff:end,:);
y_train = train_data(:,4:5);
y_test = test_data(:,4:5);
X_train = train_data(:,1:3);
X_test = test_data(:,1:3);
%%
[regressor, valid_rmse] = trainRegressionModel(train_data);%Regenerate these functions using the learner apps, whenever making changes to code
[bias,std_dev,y_hat] = predict(regressor,X_test,y_test);

%% Non-coupled extraction
data_1 = data(data(:,5)==512,[1,2,3,4]);
data_2 = data(data(:,4)==512,[1,2,3,5]);
N1 = length(data_1);
N2 = length(data_2);
%%
shuffled_1 = data_1(randperm(N1),:);
train_test_cutoff = floor(N1*train_portion);
train_data_1 = shuffled_1(1:train_test_cutoff-1,:);
test_data_1 = shuffled_1(train_test_cutoff:end,:);
shuffled_2 = data_2(randperm(N2),:);
train_test_cutoff = floor(N2*train_portion);
train_data_2 = shuffled_2(1:train_test_cutoff-1,:);
test_data_2 = shuffled_2(train_test_cutoff:end,:);
y_train_1 = train_data_1(:,4);
y_test_1 = test_data_1(:,4);
X_train_1 = train_data_1(:,1:3);
X_test_1 = test_data_1(:,1:3);
y_train_2 = train_data_2(:,4);
y_test_2 = test_data_2(:,4);
X_train_2 = train_data_2(:,1:3);
X_test_2 = test_data_2(:,1:3);


%%
disp("================Regression=================");
[regressor_1, valid_rmse_1] = trainUnivariateRegressionModel(train_data_1);%Regenerate these functions using the learner apps, whenever making changes to code

[regressor_2, valid_rmse_2] = trainUnivariateRegressionModel(train_data_2);%Regenerate these functions using the learner apps, whenever making changes to code

[bias_1,std_1,y_hat_1] = predict(regressor_1,X_test_1,y_test_1);
[bias_2,std_2,y_hat_2] = predict(regressor_2,X_test_2,y_test_2);


%%
figure
beta = mvregress(X_train,y_train);
y_hat = X_test*beta;
errors_1 = y_hat - y_test;
err_dist = mean(errors_1,2);
bias = mean(err_dist)
stdev = std(err_dist)
histfit(err_dist);
figure
y_control = 512*ones(size(y_test));
err_control = y_control - y_test;
err_dist_control = mean(err_control,2);
bias_control = mean(err_dist_control)
stdev_control = std(err_dist_control)

histfit(err_dist_control);