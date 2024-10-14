from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from helpers import *
from numpy import inf
from sklearn.preprocessing import StandardScaler
from itertools import product
# from scipy import odr

def main():
    def linear_regression(X,Y,file_path,X_label,Y_label):
        X,Y = np.array(X),np.array(Y)

        # Create a LinearRegression model and fit the data
        model = LinearRegression()

        model.fit(X.reshape(-1, 1), Y)

        # Get the slope (coef_) and intercept (intercept_)
        slope = model.coef_[0]
        intercept = model.intercept_
        print(slope)
        # Make predictions
        Y_pred = model.predict(X.reshape(-1, 1),)

        rotulo = f'Regressão: $y = {np.round(slope,7)}~x + {np.round(intercept,7)}$'
        # (Optional): Plot the data points and the regression line
        plt.scatter(X, Y, color='blue', zorder=10, label='Data Points')
        plt.plot(X, Y_pred, color='red', label=rotulo)
        plt.xlabel(X_label)
        plt.ylabel(Y_label)
        plt.title('Linear Regression using scikit-learn')
        plt.legend()
        plt.savefig(file_path)
        # plt.show()
        plt.clf()

        # Print the slope and intercept
        print(f"Slope (m): {slope}")
        print(f"Intercept (b): {intercept}")

    def log_linear_regression(input_X,input_Y,file_path,X_label,Y_label):
        X,Y = np.array(input_X),np.array(input_Y)
        X = np.log(X)
        # X = StandardScaler().fit_transform(np.log(X).reshape(-1,1)).flatten()
        # log(0) = -inf so we need to clean the bad data
        truth_table = np.abs(X) != inf
        Y = Y[truth_table]
        X = X[truth_table] 

        # Create a LinearRegression model and fit the data
        model = LinearRegression()

        model.fit(X.reshape(-1, 1), Y)

        # Get the slope (coef_) and intercept (intercept_)
        slope = model.coef_[0]
        intercept = model.intercept_
        print(slope)
        # Make predictions
        Y_pred = model.predict(X.reshape(-1, 1),)

        rotulo = f'Regressão: $y = {np.round(slope,7)}~x + {np.round(intercept,7)}$'
        plt.scatter(X, Y, color='blue', zorder=10, label='Data Points')
        plt.plot(X, Y_pred, color='red', label=rotulo)
        plt.xlabel(X_label)
        plt.ylabel(Y_label)
        plt.title('Linear Regression using scikit-learn')
        plt.legend()
        plt.savefig(file_path)
        plt.clf()

    def exp_linear_regression(input_X,input_Y,file_path,X_label,Y_label):
        X,Y = np.array(input_X),np.array(input_Y)
        X = np.exp(X)
        truth_table = (np.logical_not(np.isnan(X))) & (np.abs(X) != inf)
        X = X[truth_table]
        # X = StandardScaler().fit_transform(X.reshape(-1,1)).flatten()
        # log(0) = -inf so we need to clean the bad data
        truth_table = (np.logical_not(np.isnan(X))) & (np.abs(X) != inf)
        X = X[truth_table] 
        Y = Y[truth_table]

        # Create a LinearRegression model and fit the data
        model = LinearRegression()

        model.fit(X.reshape(-1, 1), Y)

        # Get the slope (coef_) and intercept (intercept_)
        slope = model.coef_[0]
        intercept = model.intercept_
        print(slope)
        # Make predictions
        Y_pred = model.predict(X.reshape(-1, 1),)

        rotulo = f'Regressão: $y = {np.round(slope,7)}~x + {np.round(intercept,7)}$'
        plt.scatter(X, Y, color='blue', zorder=10, label='Data Points')
        plt.plot(X, Y_pred, color='red', label=rotulo)
        plt.xlabel(X_label)
        plt.ylabel(Y_label)
        plt.title('Linear Regression using scikit-learn')
        plt.legend()
        plt.savefig(file_path)
        plt.clf()

        # Print the slope and intercept
        print(f"Slope (m): {slope}")
        print(f"Intercept (b): {intercept}")

    print('\n\n/////////////////Begin Linear Regression/////////////////\n\n')
    for plot_type,lin_reg in  zip(['raw','log'],[linear_regression,log_linear_regression]):
        # if plot_type != 'exp': continue
        print(lin_reg)
        print(f'\n\n/////////////////{plot_type} Data/////////////////\n\n')
        print('\n\n/////////////////Random Queue Analysis/////////////////\n\n')
        # print(f'x : {[x[0] for x in x_values]} , y : {[y[0] for y in rq_y_values]}')
        lin_reg([x[0] for x in x_values] ,[y[0] for y in rq_y_values],f'data-analysis/plots/{plot_type}/rq_cycle_size_throughput.png','Average Cycle Size','Throughput')
        lin_reg([x[1] for x in x_values] ,[y[0] for y in rq_y_values],f'data-analysis/plots/{plot_type}/rq_cycle_byte_size_throughput.png','Average Cycle Bytes Size','Throughput')

        # print('\n\n/////////////////Avg. Response Time Analysis/////////////////\n\n')
        lin_reg([x[0] for x in x_values] ,[y[1] for y in rq_y_values],f'data-analysis/plots/{plot_type}/rq_cycle_syze_avg_response_time.png','Average Cycle Size','Average Response Time')
        lin_reg([x[1] for x in x_values] ,[y[1] for y in rq_y_values],f'data-analysis/plots/{plot_type}/rq_cycle_byte_syze_avg_response_time.png','Average Cycle Bytes Size','Average Response Time')

        print('\n\n/////////////////Round Robin Analysis/////////////////\n\n')
        lin_reg([x[0] for x in x_values] ,[y[0] for y in rr_y_values],f'data-analysis/plots/{plot_type}/rr_cycle_size_throughput.png','Average Cycle Size','Throughput')
        lin_reg([x[1] for x in x_values] ,[y[0] for y in rr_y_values],f'data-analysis/plots/{plot_type}/rr_cycle_byte_size_throughput.png','Average Cycle Bytes Size','Throughput')

        # print('\n\n/////////////////Avg. Response Time Analysis/////////////////\n\n')
        lin_reg([x[0] for x in x_values] ,[y[1] for y in rr_y_values],f'data-analysis/plots/{plot_type}/rr_cycle_syze_avg_response_time.png','Average Cycle Size','Average Response Time')
        lin_reg([x[1] for x in x_values] ,[y[1] for y in rr_y_values],f'data-analysis/plots/{plot_type}/rr_cycle_byte_syze_avg_response_time.png','Average Cycle Bytes Size','Average Response Time')

        print('\n\n/////////////////Shortest Queue Analysis/////////////////\n\n')
        lin_reg([x[0] for x in x_values] ,[y[0] for y in sq_y_values],f'data-analysis/plots/{plot_type}/sq_cycle_size_throughput.png','Average Cycle Size','Throughput')
        lin_reg([x[1] for x in x_values] ,[y[0] for y in sq_y_values],f'data-analysis/plots/{plot_type}/sq_cycle_byte_size_throughput.png','Average Cycle Bytes Size','Throughput')

        # print('\n\n/////////////////Avg. Response Time Analysis/////////////////\n\n')
        lin_reg([x[0] for x in x_values] ,[y[1] for y in sq_y_values],f'data-analysis/plots/{plot_type}/sq_cycle_syze_avg_response_time.png','Average Cycle Size','Average Response Time')
        lin_reg([x[1] for x in x_values] ,[y[1] for y in sq_y_values],f'data-analysis/plots/{plot_type}/sq_cycle_byte_syze_avg_response_time.png','Average Cycle Bytes Size','Average Response Time')

def transform_traffic(traffic):
    number_of_cycles = 100
    total_traffic_bytes_size = 0  # total number of bytes
    total_traffic_size = 0 # total number of packets
    for k in traffic: # for each packet
        for v in traffic[k]:
            total_traffic_bytes_size +=  3*v['size']*v['type'] + 2*v['size']*(1-v['type'])
            total_traffic_size += 1
    average_cycle_size = total_traffic_size/number_of_cycles # normalize by number of cycles
    average_cycle_bytes_size = total_traffic_bytes_size/number_of_cycles # normalize by number of cycles
    print(f'average_cycle_size: {average_cycle_size} average_cycle_bytes_size: {average_cycle_bytes_size}')
    return average_cycle_size,average_cycle_bytes_size

def get_values(log):
    throughput = log['throughput']
    avg_response_time = log['avg_response_time']
    if throughput == None:
        throughput = 0
    if avg_response_time == None:
        avg_response_time = 0
    return throughput,avg_response_time

if __name__ == '__main__':
    def log_linear_regression(input_X,input_Y):
        X,Y = np.array(input_X),np.array(input_Y)
        Y_input = Y
        X = np.log(X)
        # X = StandardScaler().fit_transform(np.log(X).reshape(-1,1)).flatten()
        # log(0) = -inf so we need to clean the bad data
        truth_table = np.abs(X) != inf
        Y = Y[truth_table]
        X = X[truth_table]
        Y_input = Y_input[truth_table]

        # Create a LinearRegression model and fit the data
        model = LinearRegression()

        model.fit(X.reshape(-1, 1), Y)

        # Get the slope (coef_) and intercept (intercept_)
        slope = model.coef_[0]
        intercept = model.intercept_
        print(slope)
        # Make predictions
        Y_pred = model.predict(X.reshape(-1, 1),)
        return X,Y_input,Y_pred,slope,intercept

    def multiplot(X,Y_axe,X_label,Y_labels):
        fig=plt.figure()

        axe = fig.add_subplot(111, label="1"),fig.add_subplot(111, label="2", frame_on=False)
        for i,color in zip(range(2),['red','blue']):
            ax = axe[i]

            Y,Y_pred,a,b = Y_axe[i]
            
            rotulo = f'Regressão: $Throughput = {np.round(a,3)}~x + {np.round(b,3)}$'
            pred_color = 'indigo' if color == 'blue' else 'orangered'
            ax.scatter(X, Y, color=f"{color}")
            ax.set_xlabel(f'{X_label}', color=f"{color}")
            ax.set_ylabel(f'{Y_labels[1]}', color=f"{color}")
            ax.tick_params(axis='x', colors=f"{color}")
            ax.tick_params(axis='y', colors=f"{color}")
            if i == 1:
                ax.set_ylabel(f'{Y_labels[1]}', color=f"{color}")
                ax.xaxis.tick_top()
                ax.yaxis.tick_right()
                ax.plot(X, Y_pred, color='black', label=rotulo)
                rotulo = f'$Avg Response Time = {np.round(a,3)}~x + {np.round(b,3)}$'
            if i == 1:
                ax.set_ylabel(f'{Y_labels[1]}', color=f"{color}")
                ax.xaxis.tick_top()
                ax.yaxis.tick_right()
                rotulo = f'Regressão: $Avg Response Time = {np.round(a,3)}~x + {np.round(b,3)}$'
            

        plt.title('Linear Regression using scikit-learn')
        plt.legend()

    print('\n\n/////////////////Begin Collection/////////////////\n\n')
    traffics = [load_dict_from_json(f'./traffic/traffic{i}.json') for i in range(1000)]
    x_values = np.array([transform_traffic(traffic) for traffic in traffics])
    rq_y_values = [get_values(load_dict_from_json(f'./log/rqLoadBalancerLogTraffic{i}.json')) for i in range(1000)]
    rr_y_values = [get_values(load_dict_from_json(f'./log/rrLoadBalancerLogTraffic{i}.json')) for i in range(1000)]
    sq_y_values = [get_values(load_dict_from_json(f'./log/sqLoadBalancerLogTraffic{i}.json')) for i in range(1000)]
  
    lin_reg = log_linear_regression
    plot_type = 'xy'

    for balancing_policy, y_values in zip(['rq','rr','sq'],[rq_y_values,rr_y_values,sq_y_values]):
        for i,x_label in zip(range(2),['Average Cycle Size','Average Cycle Bytes Size']):
            X_input = [x[i] for x in x_values]
            y_labels =  ['Throughput','Average Response Time']
            Y1 = [y[0] for y in y_values]
            Y2 = [y[1] for y in y_values]
            log_x,Y1,y1_pred,slope1,intercept1 = lin_reg(X_input,Y1)
            _,Y2,y2_pred,slope2,intercept2 = lin_reg(X_input,Y2)
            X,Y = log_x,[(Y1,y1_pred,slope1,intercept1),(Y2,y2_pred,slope2,intercept2)]
            multiplot(X,Y,x_label,y_labels)
            which_x = 'avg_cycle_size' if 'Average Cycle Size' == x_label else 'avg_cycle_bytes_size'
            plt.savefig(f'data-analysis/plots/{plot_type}/{balancing_policy}_{which_x}.png')
            plt.clf()