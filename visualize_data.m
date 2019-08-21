close all
clear
clc
%%
importfile(uigetfile);
axes = 2;
X = data(:,1:3);
Y = data(:,4:5);
%%
% [coeff,score,latent,tsquared,explained,mu] = pca(X);
% [U,S,V] = svd(X);
% data_2d = U*S*V(:,1:2);
% data_orig = data;
% data = [data_2d y];
%%
states = unique(data(:,[4 5]),'rows');
N = length(states);
states_data = struct ;
state_X = {};
state_y = {};
state_mean = zeros(N,3);
state_std = zeros(N,3);

figure
t = -pi:0.01:pi;
for i = 1:length(states)
    state_data = data(data(:,4)==states(i,1),:);
    if axes == 2
        state_data = state_data(state_data(:,5)==states(i,2),:);
    end
    this_X = state_data(:,1:3);
    this_y = state_data(:,4:5);
    state_X(i) = {this_X};
    state_y(i) = {this_y};
    state_mean(i,:) = mean(this_X);
    state_std(i,:) = std(this_X);
    x = state_mean(i,2);
    y = state_mean(i,3);
    err_x = x + state_std(i,2)*cos(t);
    err_y = y + state_std(i,3)*sin(t);
    plot(err_x,err_y)
    scatter(x,y,'k');
    hold on
end

%%

for i = 1:length(states)
    figure
    plot(state_X{i})
end
