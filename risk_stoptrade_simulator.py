import pandas as pd
import numpy as np
import random

import time

from Simulator.r_list import R_val

r_value_list = R_val

number_of_trades = 70#int(len(r_value_list))
#print(number_of_trades)

number_of_simulations = 10000

min_risk_to_simulate = 0.001
max_risk_to_simulate = 0.1
risk_increment_size = 0.001

starting_equity = 170000

STARTING_STOP_TRADE = round(0.03, 2)
ENDING_STOP_TRADE = 0.07
STOP_TRADE_INCREMENT = 0.01

profit_goal = 0.2
#stop_trade = 0.07

#stop_trade_balance = starting_equity * (1 - stop_trade)
success_trade_balance = starting_equity + (starting_equity * profit_goal)
#print(stop_trade_balance)
#print(success_trade_balance)

final_equity_list = []
max_wd_percent_list = []
profit_margin_list = []

df_list = []

########################################################################################################################

def big_simulation(stop_trade):
    current_risk = min_risk_to_simulate
    stop_trade_balance = starting_equity * (1 - stop_trade)
    index = 0
    index_list = []
    ult_risk_list = []

    abort_trade = 0

    final_table = {'Init Equity': [], 'Risk': [], 'Goal %': [], 'Stop lmt %': [], 'Avg R': [], 'Expected Return': [], 'Avg Final Equity': [],
                   'Median Equity': [], 'Avg Profit %': [], 'Median Profit %': [], 'Max Lost %': [], 'Successful %': [], 'Stop Trade %': [],
                   'SUCC% - STOP%': []
                   }

    while current_risk <= max_risk_to_simulate:
        #current_risk += risk_increment_size
        print("current risk at", round(current_risk, 3), "current stop trade at", stop_trade)
        ult_risk = round(current_risk, 3)
        ult_risk_list.append(ult_risk)
        #print(ult_risk_list)
        #print(len(ult_risk_list))

        starting_equity_list = []
        final_equity_list = []
        max_wd_percent_list = []
        profit_margin_list = []
        average_r_list = []
        simulation_number_list = []
        kill_trade_percent_list = []
        final_average_r_list = []
        final_expacted_return_list = []
        avg_final_equity_list = []
        #mean_final_equity_list = []
        median_equity_list = []
        avg_profit_margin_list = []
        mean_profit_margin_lsit = []
        success_trade_percent_list = []

        expacted_return_list = []

        avg_kill_trade_percent_list = []
        avg_success_trade_percent_list = []

        result_table = {'Simulation Number': [], 'Equity': [], 'Risk': [], 'Goal %': [], 'Stop Lmt %': [], 'Average R': [], 'Avg Balance': [], 'MD %': [], 'Numbers of killed Trade':[]}

                        #'Trade Number': [], 'Risk %': [], 'Risk Equity': [],
                        #     'Balance': [],
                        #     'Max WD %': [],  , 'Stop Trade Balance': [],
                        #     'Stop Trade %': [], }

        for simulation_number in range(number_of_simulations):
            equity = int(starting_equity)
            trade = 0
            accum = 0
            kill_trade = 0

            trade_number_list = []
            random_r_list = []
            current_risk_list = []
            r_equity_list = []
            equity_list = []
            balance_list = []

            profit_goal_list = []
            stop_trade_list = []
            stop_trade_balance_list = []
            kill_trade_list = []
            kill_trade_final_list = []

            simulation_result = {'Equity': [], 'Trade Number': [], 'Risk %': [], 'Risk Equity': [], 'R': [],
                                 'Balance': [],
                                 'Max WD %': [], 'Goal %': [], 'Stop Limite %': [], 'Stop Trade Balance': [],
                                 'Stop Trade %': [], }

            # neg_r = []
            max_draw_list = []

            # while trade <= number_of_trades:
            # shuffle_r_list = random.sample(r_value_list, k=number_of_trades)

            while trade <= number_of_trades:
                current_risk_list.append(current_risk)

                profit_goal_list.append(profit_goal)
                stop_trade_list.append(stop_trade)
                stop_trade_balance_list.append(stop_trade_balance)

                random_r = random.SystemRandom()
                trade_r = random_r.choice(r_value_list)

                #trade_r = i
                # print(trade_r)
                random_r_list.append(trade_r)

                if trade_r < 0:
                    # neg_r.append(int(-1))
                    accum += trade_r
                    max_draw_list.append(round(accum, 2))
                else:
                    # neg_r.append(int(0))
                    accum = 0
                    max_draw_list.append(round(accum, 2))

                r_equity = equity * current_risk
                r_equity_list.append(round(r_equity, 2))

                trade_equity = (r_equity * trade_r)
                equity_list.append(round(equity, 2))

                equity += trade_equity
                balance_list.append(round(equity, 2))

                trade_number_list.append(trade)
                trade += 1
                #i += 1

                if equity >= stop_trade_balance:
                    kill_trade = 0
                    kill_trade_list.append(kill_trade)
                else:
                    kill_trade = 1
                    kill_trade_list.append(kill_trade)
                    break

            # print(trade_number_list)
            # print(random_r_list)
            # print(current_risk_list)
            # print(r_equity_list)
            # print(equity_list)
            # print(balance_list)

            # print(neg_r)
            # print(max_draw_list)

            simulation_result['Equity'].extend(list(equity_list))
            simulation_result['Trade Number'].extend(list(trade_number_list))
            simulation_result['Risk %'].extend(list(current_risk_list))
            simulation_result['Risk Equity'].extend(list(r_equity_list))
            simulation_result['R'].extend(list(random_r_list))
            simulation_result['Balance'].extend(list(balance_list))
            # simulation_result['0 or -1'].extend(list(neg_r))
            simulation_result['Max WD %'].extend(list(max_draw_list))

            simulation_result['Goal %'].extend(list(profit_goal_list))
            simulation_result['Stop Limite %'].extend(list(stop_trade_list))
            simulation_result['Stop Trade Balance'].extend(list(stop_trade_balance_list))
            simulation_result['Stop Trade %'].extend(list(kill_trade_list))

            #df = pd.DataFrame(simulation_result, columns=['Equity', 'Trade Number', 'Risk %', 'Risk Equity', 'R', 'Balance',
            #                                              'Max WD %', 'Goal %', 'Stop Limite %', 'Stop Trade Balance', 'Stop Trade %'],
            #                                       index=trade_number_list)
            #df = pd.DataFrame(simulation_result, columns=['Equity', 'Trade Number', 'Risk %', 'Risk Equity', 'R', 'Balance',],
            #                                       index=trade_number_list)
            #                                              'Max WD %', 'Goal %', 'Stop Limite %', 'Stop Trade Balance', 'Stop Trade %'],

            #print(df)

            #if abort_trade == 0:
            #    final_equity = balance_list[-1]
            #else:
            #    final_equity = min(balance_list,)

            #elif abort_trade ===
            final_equity = balance_list[-1]
            #print("final eqt",final_equity)

            max_wd_percent = min(max_draw_list)
            average_r = np.average(random_r_list)
            profit_margin = (final_equity - starting_equity) / starting_equity
            kill_trade_final = sum(kill_trade_list)

            #print(final_equity)
            #print(max_wd_percent)
            #print(average_r)
            #print(profit_margin)
            #print("kill trade final", kill_trade_final)
            if kill_trade_final == 0:
                kill_trade_percent_list.append(0)
            else:
                kill_trade_percent_list.append(1)

            if profit_margin >= profit_goal:
                success_trade_percent_list.append(1)
            else:
                success_trade_percent_list.append(0)
            #print("killed trade percent list", kill_trade_percent_list)
            #print("number of kill", len(kill_trade_percent_list))

            #print("Success trade percent list",success_trade_percent_list)
            #print("num of success trade", len(success_trade_percent_list))

            starting_equity_list.append(starting_equity)
            final_equity_list.append(final_equity)
            max_wd_percent_list.append(max_wd_percent)
            profit_margin_list.append(profit_margin)
            average_r_list.append(average_r)
            kill_trade_final_list.append(kill_trade_final)
            simulation_number_list.append(simulation_number)

            #print("average r list",average_r_list)
            #print("number of average r", len(average_r_list))

        #print(starting_equity_list)
        #print(final_equity_list)
        #print(max_wd_percent_list)
        #print(profit_margin_list)
        #print(average_r_list)
        #print("kill trade final list",kill_trade_final_list)

        #print(simulation_number_list)

        #print("killtrade final",kill_trade_final)

        result_table['Simulation Number'].extend(simulation_number_list)
        result_table['Equity'].extend(starting_equity_list)
        result_table['Avg Balance'].extend(final_equity_list)
        result_table['Average R'].extend(average_r_list)
        result_table['MD %'].extend(max_wd_percent_list)
        result_table['Numbers of killed Trade'].extend(kill_trade_percent_list)

        #middle_df = pd.DataFrame(result_table, columns=['Simulation Number', 'Equity', 'Average R', 'Avg Balance', 'MD %', 'Numbers of killed Trade'], index=simulation_number_list)

        #print(middle_df)

        index_list.append(index)
        index += 1

        max_neg_r = min(max_wd_percent_list)
        #print(max_wd_percent_list)
        #print(max_neg_r)
        success_trade_percent = sum(success_trade_percent_list) / number_of_simulations
        #print("success_trade_percent",success_trade_percent)

        kill_trade_percent = sum(kill_trade_percent_list) / number_of_simulations
        #print("kill trade percent", kill_trade_percent)

        #avg_kill_trade_percent_list.append(kill_trade_percent)
        #avg_success_trade_percent_list.append(success_trade_percent)
        #for i in average_r_list:
        #    expacted_return = i * ult_risk
            #print(i, ult_risk, expacted_return)
         #   expacted_return_list.append(expacted_return)

        #final_expacted_return_list = np.average(expacted_return_list)

        #print(average_r_list)
        final_average_r_list = np.average(average_r_list)
        #print("final average r", final_average_r_list)

        avg_profit_margin_list = np.average(profit_margin_list)
        mean_profit_margin_list = np.mean(profit_margin_list)
        median_profit_margin_list = np.median(profit_margin_list)
        #print("finalaverage len", len(final_average_r_list))
        #print(final_equity_list)
        avg_final_equity_list = np.average(final_equity_list)
        #print("avg final eqt list", avg_final_equity_list)
        #mean_final_equity_list = np.mean(final_equity_list)

        median_equity_list = np.median(final_equity_list)




        #print(expacted_return_list)
        #expacted_return = average_r_list * ult_risk
        #print(expacted_return)
        #print("median eqt list",median_equity_list)
        #print("avg final eqt len", len(avg_final_equity_list))

        #print("total num of stop trade",total_num_of_stop_trade)

        #total_num_of_stop_trade = sum(total_num_of_stop_trade)
        #print("")
        #final_stop_trade_percent = total_num_of_stop_trade / range(number_of_simulations)

        final_table['Init Equity'].append(round(starting_equity, 2))
        final_table['Risk'].append(ult_risk)
        final_table['Goal %'].append(profit_goal)
        final_table['Stop lmt %'].append(stop_trade)
        final_table['Avg R'].append(round(final_average_r_list, 4))
        #final_table['Expacted Return'].append(final_expacted_return_list)
        final_table['Expected Return'].append(final_average_r_list * ult_risk)



        final_table['Avg Final Equity'].append(round(avg_final_equity_list, 2))
        #final_table['Mean Final Equity'].append(round(mean_final_equity_list))
        final_table['Median Equity'].append(round(median_equity_list,2))
        final_table['Avg Profit %'].append(round(avg_profit_margin_list, 4))
        #final_table['Mean Profit %'].append(round((mean_profit_margin_list), 4))

        final_table['Median Profit %'].append(median_profit_margin_list)#round((mean_profit_margin_list), 4))



        final_table['Max Lost %'].append(max_neg_r*ult_risk)

        #print("max_neg_r*ult_risk", max_neg_r*ult_risk)
        #final_table['Max Neg R'].append(max_neg_r)
        final_table['Stop Trade %'].append(kill_trade_percent)
        final_table['Successful %'].append(success_trade_percent)
        final_table['SUCC% - STOP%'].append(success_trade_percent-kill_trade_percent)
        #print("success_trade_percent-kill_trade_percent", success_trade_percent-kill_trade_percent)
        current_risk += risk_increment_size
        current_risk = round(current_risk, 3)

    final_df = pd.DataFrame(final_table, columns=['Init Equity', 'Risk', 'Goal %', 'Stop lmt %', 'Avg R', 'Expected Return', 'Avg Final Equity',
                                                  'Median Equity', 'Avg Profit %', 'Median Profit %', 'Max Lost %', 'Successful %', 'Stop Trade %', 'SUCC% - STOP%']
                                       , index=index_list)

    final_df.to_csv('PythonExport.csv', sep=',')
    #print(final_df)
    return final_df

start_time = time.time()

def excel_writer(STARTING_STOP_TRADE):
    stop_trade = STARTING_STOP_TRADE
    w = pd.ExcelWriter('risk_stop_simulator.xlsx')
    while stop_trade <= ENDING_STOP_TRADE:
        df = pd.DataFrame(big_simulation(stop_trade))#big_simulation(stop_trade)
        print(stop_trade,' / ', ENDING_STOP_TRADE)
        df.to_excel(w, sheet_name='stop trade_'+str(round(stop_trade,2)))
        stop_trade += STOP_TRADE_INCREMENT
        w.save()
    print('done')

excel_writer(STARTING_STOP_TRADE)
#big_simulation(0.07)
print("--- %s seconds ---" % (time.time() - start_time))