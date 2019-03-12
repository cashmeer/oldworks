def Switch_Max():
    next_max_val = 0
    internal_sell_max = 0
    internal_buy_min = 0
    internal_max = []
    internal_min = []
    for e, h, l, p in zip(event_list,high_list,low_list,posit_list):
        print(internal_min, e, p)
        print(internal_max, e, p)
        if e == 0 and p == 'buy':
            internal_min.append(l)
            internal_buy_min = min(list(internal_min))
            print('maxmax', internal_buy_min)
            switch_max.append(0)
        elif e == 0 and p == 'sell':
            #print(internal_max, e, p)
            internal_max.append(h)
            internal_sell_max = max(list(internal_max))
            print('sellmax', internal_sell_max)
            switch_max.append(0)
        else:
            switch_max = []
            print(h, next_max_val, p)
            # open = float(max(h, next_max[-1]))
            # next_max_val =  9999#float(max(h, next_max_val))
            #  next_max.append(internal_max_max)
            next_max.append(internal_max_max)


    for b, h, p in zip(bb_list, high_list, posit_list):

        #internal_max_max = max(list(internal_max))
        print(internal_max, p)
        #print(internal_max_max)
        if b == 0:
            high = h
            internal_max.append(high)
            internal_max_max = max(list(internal_max))
            print('maxmax',internal_max_max)
            next_max.append(0)
        else:
            internal_max = []
            print(h, next_max_val , p)
            #open = float(max(h, next_max[-1]))
            #next_max_val =  9999#float(max(h, next_max_val))
         #  next_max.append(internal_max_max)
            next_max.append(internal_max_max)
    print(next_max)