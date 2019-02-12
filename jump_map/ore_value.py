from prices import amarr_price_now, mineralID
from math import floor

def rep_kernite(volume, unit = "m3", efficiency = 0.691, type = "N"):
    # type is "N" normal, "F" fiery, "L" luminous
    # unit can be "m3" volume, or "n" number

    if unit == "m3":
        n_units = floor(volume / 1.2)
    if unit == "n":
        n_units = volume

    process_batch = floor(n_units / 100)

    # Number of minerals reprocessed from a bath of 100 minerals:
    # https://wiki.eveuniversity.org/Asteroids_and_ore#Ore_Chart
    process_dict = {'TRI': process_batch * 134,
                    'MEX': process_batch * 267,
                    'ISO': process_batch * 134}

    if type == "L":
        for key, value in process_dict.items():
            process_dict[key] = floor(value * 1.05)

    if type == "F":
        for key, value in process_dict.items():
            process_dict[key] = floor(value * 1.10)

    for key, value in process_dict.items():
        process_dict[key] = floor(value * efficiency)

    sell_prices = []
    for key, value in process_dict.items():
        # mineralID gives the typeID of the mineral abbreviation,
        # amarr_price_now with type = "sell" gives me best buy order in Amarr
        sell_price = amarr_price_now(mineralID(key), type="sell") * value
        sell_prices.append(round(sell_price))

    total_value = sum(sell_prices)
    return(total_value)

def sell_kernite(volume, unit = "m3", type = "N"):
    # type is "N" normal, "F" fiery, "L" luminous
    # unit can be "m3" volume, or "n" number

    if unit == "m3":
        n_units = floor(volume / 1.2)
    if unit == "n":
        n_units = volume

    if type == "N":
        ID_ = 20
    if type == "F":
        ID_ = 17453
    if type == "L":
        ID_ = 17452

    sell_price = amarr_price_now(ID = ID_, type="sell") * n_units
    return(round(sell_price))



def rep_pyro(volume, unit = "m3", efficiency = 0.691, type = "N"):
    # type is "N" normal, "S" solid, "V" viscous
    # unit can be "m3" volume, or "n" number

    if unit == "m3":
        n_units = floor(volume / 0.3)
    if unit == "n":
        n_units = volume

    process_batch = floor(n_units / 100)

    # Number of minerals reprocessed from a bath of 100 minerals:
    # https://wiki.eveuniversity.org/Asteroids_and_ore#Ore_Chart
    process_dict = {'TRI': process_batch * 351,
                    'MEX': process_batch * 50,
                    'PYE': process_batch * 25,
                    'NOC': process_batch * 5}

    if type == "S":
        for key, value in process_dict.items():
            process_dict[key] = floor(value * 1.05)

    if type == "V":
        for key, value in process_dict.items():
            process_dict[key] = floor(value * 1.10)

    for key, value in process_dict.items():
        process_dict[key] = floor(value * efficiency)

    sell_prices = []
    for key, value in process_dict.items():
        # mineralID gives the typeID of the mineral abbreviation,
        # amarr_price_now with type = "sell" gives me best buy order in Amarr
        sell_price = amarr_price_now(mineralID(key), type="sell") * value
        sell_prices.append(round(sell_price))

    total_value = sum(sell_prices)
    return(total_value)

def sell_pyro(volume, unit = "m3", type = "N"):
    # type is "N" normal, "S" solid, "V" viscous
    # unit can be "m3" volume, or "n" number

    if unit == "m3":
        n_units = floor(volume / 1.2)
    if unit == "n":
        n_units = volume

    if type == "N":
        ID_ = 1224
    if type == "S":
        ID_ = 17459
    if type == "V":
        ID_ = 17460

    sell_price = amarr_price_now(ID = ID_, type="sell") * n_units
    return(round(sell_price))


# Worth most is kernite to sell, then any type of pyroxeres to reprocess