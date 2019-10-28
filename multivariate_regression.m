clear;
%% Get data
fname = uigetfile("../data/automated/")
load('-mat',fname);
N = length(data);
Xs = data(:,1:3);
ys = data(:,4:5);

%% Get baselines
train_portion = 0.8;
% neutral_y1 = data(:,4)== 512;
% data_ny1 = data(neutral_y1,:);
% neutral_y2 = data_ny1(:,5) == 512;
% data_neutral = data_ny1(neutral_y2,:);
% neutral_mean = mean(data_neutral);
% neutral_x = neutral_mean(1:3);
% old_data = data;
% data = [data(:,1:end-2)-neutral_x, data(:,end-1:end)];
    
%% Pre-process data set
shuffled = data(randperm(N),:);
train_test_cutoff = floor(N*train_portion);
train_data = shuffled(1:train_test_cutoff-1,:);
test_data = shuffled(train_test_cutoff:end,:);
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
[regressor_mimo1, valid_rmse_mimo1] = trainUnivariateRegressionModel([X_train,y_train(:,1)]);%Regenerate these functions using the learner apps, whenever making changes to code
[regressor_mimo2, valid_rmse_mimo2] = trainUnivariateRegressionModel([X_train,y_train(:,2)]);%Regenerate these functions using the learner apps, whenever making changes to code
    %% MIMO1
disp("Axis 1:");
[bias_mimo1,std_mimo1,y_hat_mimo1] = predict(regressor_mimo1,X_test,y_test(:,1));
%title("Univariate model: Multimodal axis 1 > Multimodal axis 1")
disp("Axis 2:");
[bias_mimo2,std_mimo2,y_hat_mimo2] = predict(regressor_mimo2,X_test,y_test(:,2));
%title("Univariate model: Multimodal axis 2 > Multimodal axis 2")

% %%
% disp('training pipo1')
% [regressor_pipo1, valid_rmse_pipo1] = trainUnivariateRegressionModel(train_data_1);%Regenerate these functions using the learner apps, whenever making changes to code
% disp('training pipo2')
% [regressor_pipo2, valid_rmse_pipo2] = trainUnivariateRegressionModel(train_data_2);%Regenerate these functions using the learner apps, whenever making changes to code
% 
% %% MIPO1
% disp("MIPO 1:");
% [bias_mipo1,std_mipo1,y_hat_mipo1] = predict(regressor_mimo1,X_test_1,y_test_1);
% %title("Univariate model: Multimodal axis 1 > Pure axis 1")
% disp("MIPO 2:");
% [bias_mipo2,std_mipo2,y_hat_mipo2] = predict(regressor_mimo2,X_test_2,y_test_2);
% %title("Univariate model: Multimodal axis 2 > Pure axis 2")
% %% PIPO 1
% disp("PIPO 1:");
% [bias_pipo1,std_pipo1,y_hat_pipo1] = predict(regressor_pipo1,X_test_1,y_test_1);
% %title("Univariate model: Pure axis 1 > Pure axis 1")
% disp("PIPO 2:");
% [bias_pipo2,std_pipo2,y_hat_pipo2] = predict(regressor_pipo2,X_test_2,y_test_2);
% %title("Univariate model: Pure axis 2 > Pure axis 2")
% %% PIMO 1
% disp("PIMO 1:");
% [bias_pimo1,std_pimo1,y_hat_pimo1] = predict(regressor_pipo1,X_test,y_test(:,1));
% %title("Univariate model: Pure axis 1 > Multimodal axis 1")
% disp("PIMO 2:");
% [bias_pimo2,std_pimo2,y_hat_pimo2] = predict(regressor_pipo2,X_test,y_test(:,2));
% %title("Univariate model: Pure axis 2 > Multimodal axis 2")

%% Compare

%bar_labels = categorical({'pipo', 'mipo', 'mimo', 'pimo'},{'pipo', 'mipo', 'mimo', 'pimo'});
% biases = [bias_pipo1, bias_pipo2; bias_mimo1, bias_mimo2; bias_pimo1, bias_pimo2; bias_mvar1, bias_mvar2; bias_neural1, bias_neural2];
% figure
% bar(bar_labels,abs(biases))
%std_deviations = [std_pipo1, std_pipo2; std_mipo1, std_mipo2; std_mimo1, std_mimo2; std_pimo1, std_pimo2];
% figure
% bar(bar_labels,(std_deviations)*99/100)
% title('RMSE across different mappings')
% ylabel('RMSE (servo ticks)')
%% Examine Data
figure
scatter3(Xs(:,1),Xs(:,2),Xs(:,3),20,ys(:,1),'filled')
colormap('jet')
colorbar
xlabel("Magnetometer X")
ylabel("Magnetometer Y")
zlabel("Magnetometer Z")
figure
scatter3(Xs(:,1),Xs(:,2),Xs(:,3),20,ys(:,2),'filled')
colormap('jet')
colorbar
xlabel("Magnetometer X")
ylabel("Magnetometer Y")
zlabel("Magnetometer Z")
