def to_unicode(token):
    if isinstance(token, tuple):
        return tuple(item.encode('unicode_escape').decode() for item in token)
    return token.encode('unicode_escape').decode()


def levenshtein_distance(y_test, y_pred, debug=False):
    n = len(y_test)
    m = len(y_pred)

    dp = [[0 for _ in range(m+1)] for _ in range(n+1)]

    for i in range(n+1):
        dp[i][0] = i

    for j in range(m+1):
        dp[0][j] = j

    for i in range(n):
        for j in range(m):
            sub_cost = dp[i][j]
            del_cost = dp[i+1][j] + 1
            add_cost = dp[i][j+1] + 1

            if y_test[i] != y_pred[j]:
                sub_cost += 1

            dp[i+1][j+1] = min(sub_cost, del_cost, add_cost)

    if debug:
        for row in dp:
            print(row)

    return dp[n][m]


def character_error_rate(y_test, y_pred):
    n = len(y_test)
    m = len(y_pred)
    levenshtein = levenshtein_distance(y_test, y_pred)

    return levenshtein / max(n, m)
