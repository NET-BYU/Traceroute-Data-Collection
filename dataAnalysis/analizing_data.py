import data_manipulation
from loguru import logger


def detection(id1, id2, t1, t2, truth):
    # when doing in real time pause while traceroute collects data
    testing1, testing2 = data_manipulation.gap_detected(id1, id2, t1, t2, truth)
    score = traceroute_analysis(testing1, testing2)
    # Score will show how many trigered true of false. If we are checking for true values that is the accuracy. If we are checking against false data we have to invert the score. (score = 0 means that it was 100% accurate)
    return score


# Parses all of the data and puts it in a variable called data
def traceroute_analysis(good_data, unverified_data):
    good_data = data_manipulation.trim_dataframe(good_data, 6)
    unverified_data = data_manipulation.trim_dataframe(unverified_data, 6)
    verify_check = data_manipulation.create_check(good_data)
    verified_data = []
    total_true = 0
    for i in unverified_data.index:
        verified_data.append(verify(unverified_data.take([i], axis=0), verify_check))
        total_true += verified_data[i]
    reliability_percent = total_true / len(verified_data)

    return reliability_percent


def verify(data, verify_check):
    traceroute_score = 0.0
    # delay_score = 0.0
    if len(data.iat[0, 0]) <= len(verify_check[0]):
        for i in range(len(data.iat[0, 0])):
            # Checks every datapoint in Traceroute to see if it is in verify check. If it is in the exact same place, give it a higher score
            if data.iat[0, 0][i] in verify_check[0][i]:
                traceroute_score += 1
    else:
        for i in range(len(verify_check[0])):
            # Does the same thing as the if statement, just not going out of bounds. I am not convinced this redundancy is nessisary, however I put it in here because I was having problems
            if data.iat[0, 0][i] in verify_check[0][i]:
                traceroute_score += 1

    # This entire section is using latency measurements as a factor in the evaluation
    # try:
    # Checks to see if the delay we have gotten is within 1 standard deveations of the verify_check data
    # Once again there is the length redudnancy because I am having mysterious errors sometimes
    # sandard_deviations = 1
    # if len(data.iat[1, 0]) <= len(verify_check[1]):
    #     for i in range(len(data.iat[0, 1])):
    #         if data.iat[0, 1][i] >= (
    #             verify_check[1][i][1] - sandard_deviations * verify_check[1][i][0]
    #         ) and data.iat[0, 1][i] <= (
    #             verify_check[1][i][1] + sandard_deviations * verify_check[1][i][0]
    #         ):
    #             delay_score += 1
    # else:
    #     for i in range(len(verify_check[1])):
    #         if data.iat[0, 1][i] >= (
    #             verify_check[1][i][1] - sandard_deviations * verify_check[1][i][0]
    #         ) and data.iat[0, 1][i] <= (
    #             verify_check[1][i][1] + sandard_deviations * verify_check[1][i][0]
    #         ):
    #             delay_score += 1
    # except:
    #     logger.debug("Error comparing delay data")
    #     return "Two"
    total_score = traceroute_score / len(
        data.iat[0, 0]
    )  # * 0.8 + (delay_score / len(data.iat[0, 0])) * 0.2                #This makes the IP addresses worth 80% of the total score and the delay data worth 20% of the total score
    return total_score
