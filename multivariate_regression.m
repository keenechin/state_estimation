close all
clear
clc
%% Get data
importfile(uigetfile('D:\Drive\desktop\research\shape_tracking\data\automated\*.mat'));
N = length(data);
Xs = data(:,1:3);
ys = data(:,4:5);
%% Pre-process data set
train_portion = 0.8;

shuffled = data(randperm(N),:);
train_test_cutoff = floor(N*train_portion);
train_data = shuffled(1:train_test_cutoff-1,:);
test_data = shuffled(train_test_cutoff:end,:);
y_train = train_data(:,4:5);
y_test = test_data(:,4:5);
X_train = train_data(:,1:3);
X_test = test_data(:,1:3);

%% Non-coupled pre-processing

data_1 = data(data(:,5)==512,[1,2,3,4]);
data_2 = data(data(:,4)==512,[1,2,3,5]);
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
y_train_1 = train_data_1(:,4);
y_test_1 = test_data_1(:,4);
X_train_1 = train_data_1(:,1:3);
X_test_1 = test_data_1(:,1:3);
y_train_2 = train_data_2(:,4);
y_test_2 = test_data_2(:,4);
X_train_2 = train_data_2(:,1:3);
X_test_2 = test_data_2(:,1:3);
%% Train models
disp('training mimo1')
[regressor_mimo1, valid_rmse_mimo1] = trainUnivariateRegressionModel([X_train,y_train(:,1)]);%Regenerate these functions using the learner apps, whenever making changes to code
disp('training mimo2')
[regressor_mimo2, valid_rmse_mimo2] = trainUnivariateRegressionModel([X_train,y_train(:,2)]);%Regenerate these functions using the learner apps, whenever making changes to code
disp('training pipo1')
[regressor_pipo1, valid_rmse_pipo1] = trainUnivariateRegressionModel(train_data_1);%Regenerate these functions using the learner apps, whenever making changes to code
disp('training pipo2')
[regressor_pipo2, valid_rmse_pipo2] = trainUnivariateRegressionModel(train_data_2);%Regenerate these functions using the learner apps, whenever making changes to code
disp('mvregress')
beta = mvregress(X_train,y_train);

%% MIMO1
disp("MIMO 1:");
[bias_mimo1,std_mimo1,y_hat_mimo1] = predict(regressor_mimo1,X_test,y_test(:,1));
title("Univariate model: Multimodal axis 1 > Multimodal axis 1")
%% MIMO2
disp("MIMO 2:");
[bias_mimo2,std_mimo2,y_hat_mimo2] = predict(regressor_mimo2,X_test,y_test(:,2));
title("Univariate model: Multimodal axis 2 > Multimodal axis 2")

%% MIPO1
disp("MIPO 1:");
[bias_mipo1,std_mipo1,y_hat_mipo1] = predict(regressor_mimo1,X_test_1,y_test_1);
title("Univariate model: Multimodal axis 1 > Pure axis 1")
%% MIPO2
disp("MIPO 2:");
[bias_mipo2,std_mipo2,y_hat_mipo2] = predict(regressor_mimo2,X_test_2,y_test_2);
title("Univariate model: Multimodal axis 2 > Pure axis 2")
%% PIPO 1
disp("PIPO 1:");
[bias_pipo1,std_pipo1,y_hat_pipo1] = predict(regressor_pipo1,X_test_1,y_test_1);
title("Univariate model: Pure axis 1 > Pure axis 1")
%% PIPO 2
disp("PIPO 2:");
[bias_pipo2,std_pipo2,y_hat_pipo2] = predict(regressor_pipo2,X_test_2,y_test_2);
title("Univariate model: Pure axis 2 > Pure axis 2")
%% PIMO 1
disp("PIMO 1:");
[bias_pimo1,std_pimo1,y_hat_pimo1] = predict(regressor_pipo1,X_test,y_test(:,1));
title("Univariate model: Pure axis 1 > Multimodal axis 1")
%% PIMO 2
disp("PIMO 2:");
[bias_pimo2,std_pimo2,y_hat_pimo2] = predict(regressor_pipo2,X_test,y_test(:,2));
title("Univariate model: Pure axis 2 > Multimodal axis 2")
%% MVAR
disp("MVAR Axis 1:");
y_hat_mvar = X_test*beta;
errors_mvar = y_hat_mvar - y_test;
errors_mvar1 = errors_mvar(:,1);
bias_mvar1 = mean(errors_mvar1);
std_mvar1 = std(errors_mvar1);
figure
histfit(errors_mvar1);
xlabel("Position error")
ylabel("Number of test samples")
title("Multivariate model: Multimodal grid > Multimodal data axis 1")
disp("Prediction bias: "+bias_mvar1);
disp("Prediction standard deviation: "+std_mvar1);
disp("");
disp("MVAR Axis 2:");
errors_mvar2 = errors_mvar(:,2);
bias_mvar2 = mean(errors_mvar2);
std_mvar2 = std(errors_mvar2);
figure
histfit(errors_mvar2);
xlabel("Position error")
ylabel("Number of test samples")
title("Multivariate model: Multimodal grid > Multimodal data axis 2")
disp("Prediction bias: "+bias_mvar2);
disp("Prediction standard deviation: "+std_mvar2);
disp("");
disp("");



%% MVAR Neural
disp("Neural MVAR Axis 1:");
y_hat_neural = multivariateNeuralNetTrained(X_test);
errors_neural = y_hat_neural - y_test;
errors_neural1 = errors_neural(:,1);
bias_neural1 = mean(errors_neural1);
std_neural1 = std(errors_neural1);
figure
histfit(errors_neural1);
xlabel("Position error")
ylabel("Number of test samples")
title("Multivariate NN model: Multimodal grid > Multimodal data axis 1")
disp("Prediction bias: "+bias_neural1);
disp("Prediction standard deviation: "+std_neural1);
disp("");
disp("Neural MVAR Axis 2:");
errors_neural2 = errors_neural(:,2);
bias_neural2 = mean(errors_neural2);
std_neural2 = std(errors_neural2);
figure
histfit(errors_neural2);
xlabel("Position error")
ylabel("Number of test samples")
title("Multivariate NN model: Multimodal grid > Multimodal data axis 2")
disp("Prediction bias: "+bias_neural2);
disp("Prediction standard deviation: "+std_neural2);
disp("");

%% Compare

bar_labels = categorical({'pipo', 'mipo', 'mimo', 'pimo', 'mvar'},{'pipo', 'mipo', 'mimo', 'pimo', 'mvar'});
% biases = [bias_pipo1, bias_pipo2; bias_mimo1, bias_mimo2; bias_pimo1, bias_pimo2; bias_mvar1, bias_mvar2; bias_neural1, bias_neural2];
% figure
% bar(bar_labels,abs(biases))
std_deviations = [std_pipo1, std_pipo2; std_mipo1, std_mipo2; std_mimo1, std_mimo2; std_pimo1, std_pimo2; std_mvar1, std_mvar2];
figure
bar(bar_labels,(std_deviations)*99/100)
title('RMSE across different mappings')
ylabel('RMSE (servo ticks)')
%%
figure
scatter3(Xs(:,1),Xs(:,2),Xs(:,3),20,ys(:,1),'filled')
colormap('jet')
colorbar
figure
scatter3(Xs(:,1),Xs(:,2),Xs(:,3),20,ys(:,2),'filled')
colormap('jet')
colorbar
%% MVAR Control
% disp("MVAR Control:");
% y_control = 512*ones(size(y_test));
% err_control = y_control - y_test;
% errors_control = mean(err_control,2);
% bias_control = mean(errors_control);
% stdev_control = std(errors_control);
% figure
% histfit(errors_control);
% xlabel("Position error")
% ylabel("Number of test samples")
% title("Distribution of errors for position classification")
% disp("Prediction bias: "+bias_control);
% disp("Prediction standard deviation: "+stdev_control);
% disp("");
% disp("");