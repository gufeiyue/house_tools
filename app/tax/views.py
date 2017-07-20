# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import render_template, request, redirect, url_for, flash, jsonify
from . import tax
import re

@tax.route('/commercial_loan', methods=['GET', 'POST'])
def commercial_loan():
    return render_template('tax/commercial_loan.html')


@tax.route('/provident_fund_loan', methods=['GET', 'POST'])
def provident_fund_loan():
    return render_template('tax/provident_fund_loan.html')


@tax.route('/combination_loan', methods=['GET', 'POST'])
def combination_loan():
    return render_template('tax/combination_loan.html')


@tax.route('/commercial_calc', methods=['GET', 'POST'])
def commercial_calc():
    loan_total = request.form.get('loan_total')
    loan_year = request.form.get('loan_year')
    annual_rate_percent = request.form.get('loan_rate')

    loan_year = int(loan_year)
    annual_rate_percent = float(annual_rate_percent)
    loan_total = float(loan_total)
    loan_total = loan_total * 10000

    # loan_year = int(re.sub("\D", "", loan_year))
    # 还款月数
    loan_month = loan_year * 12

    # 年利率
    # annual_rate_list = re.findall(r"\((.*)\%\)", annual_rate)
    annual_rate = annual_rate_percent / 100

    # 月利率
    monthly_rate = annual_rate / 12

    average_interest_list = equal_interest(loan_month, loan_total, monthly_rate)
    average_capital_list = equal_principal(loan_month, loan_total, monthly_rate)

    debj_dict = debj_list(loan_total, monthly_rate, loan_month, annual_rate_percent)
    debx_dict = debx_list(loan_total, monthly_rate, loan_month, annual_rate_percent)

    return render_template('tax/loan_result.html', average_capital_list=average_capital_list, \
                           average_interest_list=average_interest_list, debx_dict=debx_dict, debj_dict=debj_dict)


def debj_list(loan_total, monthly_rate, loan_month, annual_rate_percent):
    # 等额本金
    debj_first_month = loan_total / loan_month + loan_total * monthly_rate
    debj_total_interest = (loan_month + 1) * loan_total * monthly_rate / 2
    debj_total = debj_total_interest + loan_total

    debj_first_month = float('%.2f' % debj_first_month)
    debj_total_interest = float('%.2f' % debj_total_interest)
    debj_total = float('%.2f' % debj_total)

    debj_dict = {'debj_first_month': debj_first_month, 'debj_total_interest': debj_total_interest,\
                 'debj_total': debj_total, 'loan_total': loan_total, 'annual_rate': annual_rate_percent}
    return debj_dict


def debx_list(loan_total, monthly_rate, loan_month, annual_rate_percent):
    # 等额本息
    debx_first_month = (loan_total * monthly_rate * (1 + monthly_rate) ** loan_month) / ((1 + monthly_rate) ** loan_month - 1)
    debx_total_interest = debx_first_month * loan_month - loan_total
    debx_total = debx_total_interest + loan_total

    debx_first_month = float('%.2f' % debx_first_month)
    debx_total_interest = float('%.2f' % debx_total_interest)
    debx_total = float('%.2f' % debx_total)

    debx_dict = {'debx_first_month': debx_first_month, 'debx_total_interest': debx_total_interest, \
                 'debx_total': debx_total, 'loan_total': loan_total, 'annual_rate': annual_rate_percent}
    return debx_dict



@tax.route('/chart_list', methods=['GET', 'POST'])
def chart_list():

    chart_list = [['Safari',    50],['Opera',     5]]
    return jsonify({
        'data': chart_list
    })

# 等额本金
# 每月还本付息金额=(本金/还款月数)+(本金-累计已还本金)×月利率
# 每月本金=总本金/还款月数
# 每月利息=(本金-累计已还本金)×月利率
# 还款总利息=（还款月数+1）*贷款额*月利率/2
# 还款总额=(还款月数+1)*贷款额*月利率/2+贷款额

def equal_principal(loan_month, loan_total, monthly_rate):
    # 每月还款本金
    monthly_principal = loan_total / loan_month

    # 还款总利息
    total_interest = (loan_month + 1) * loan_total * monthly_rate / 2

    # 还款总额
    total_repayment = total_interest + loan_total

    residual_loan = total_repayment

    i = 0
    average_capital_list = []
    while i < loan_month :
        monthly_interest = (loan_total - monthly_principal * i) * monthly_rate
        monthly_total = monthly_principal + monthly_interest
        residual_loan = residual_loan - monthly_total

        monthly_total = float('%.2f' % monthly_total)
        monthly_principal = float('%.2f' % monthly_principal)
        monthly_interest = float('%.2f' % monthly_interest)
        residual_loan = float('%.2f' % residual_loan)

        average_capital = {'monthly_total': monthly_total, 'monthly_principal': monthly_principal, 'monthly_interest': monthly_interest, 'residual_loan': residual_loan}
        average_capital_list.append(average_capital)
        i = i + 1
    return average_capital_list


# 等额本息
# 每月还本付息金额 =[ 本金*月利率*(1+月利率)贷款月数 ]/[(1+月利率)还款月数 - 1]
# 还款总利息=贷款额*贷款月数*月利率*(1+月利率)贷款月数/[(1+月利率)还款月数 - 1] -贷款额
# 还款总额=还款月数*贷款额*月利率*(1+月利率)贷款月数/[(1+月利率)还款月数 - 1]
# 每月利息 = 剩余本金*贷款月利率
# 贷款本金×月利率×〔(1+月利率)^还款月数-(1+月利率)^(还款月序号-1)〕÷〔(1+月利率)^还款月数-1〕
# 每月本金=月供-每月利息
# 每月应还本金=贷款本金×月利率×(1+月利率)^(还款月序号-1)÷〔(1+月利率)^还款月数-1〕

def equal_interest(loan_month, loan_total, monthly_rate):
    # 每月还本付息金额
    monthly_total = (loan_total * monthly_rate * (1 + monthly_rate) ** loan_month) / ((1 + monthly_rate ) ** loan_month - 1)
    #print monthly_total
    print "monthly_total = " + str(monthly_total)
    # 还款总利息
    total_interest = monthly_total * loan_month - loan_total
    print "total_interest = " + str(total_interest)

    # 还款总额
    total_repayment = total_interest + loan_total
    print "total_repayment = " + str(total_repayment)

    residual_loan = total_repayment


    i = 0
    average_interest_list = []
    while i < loan_month:
        i = i + 1
        # print "i:" + str(i)
        # 每月还款利息
        monthly_interest = loan_total * monthly_rate * ((1 + monthly_rate) ** loan_month - (1 + monthly_rate) ** (i - 1)) / ((1 + monthly_rate) ** loan_month - 1)
        # 每月还款本金
        monthly_principal = monthly_total - monthly_interest
        residual_loan = residual_loan - monthly_total

        monthly_total = float('%.2f' % monthly_total)
        monthly_principal = float('%.2f' % monthly_principal)
        monthly_interest = float('%.2f' % monthly_interest)
        residual_loan = float('%.2f' % residual_loan)

        average_interest = {'monthly_total': monthly_total, 'monthly_principal': monthly_principal,
                           'monthly_interest': monthly_interest, 'residual_loan': residual_loan}
        average_interest_list.append(average_interest)

    return average_interest_list


@tax.route('/provident_fund_clac', methods=['GET', 'POST'])
def provident_fund_clac():
    return render_template('tax/loan_result.html')


@tax.route('/combination_clac', methods=['GET', 'POST'])
def combination_clac():
    return render_template('tax/loan_result.html')





@tax.route('/purchase', methods=['GET', 'POST'])
def purchase():
    return render_template('tax/purchase.html')


@tax.route('/test4', methods=['GET', 'POST'])
def test4():
    return render_template('tax/test4.html')


@tax.route('/tax_cal', methods=['GET', 'POST'])
def tax_cal():
    buyerfirsthouse = request.form.get('buyerfirsthouse')
    selleronlyhouse = request.form.get('selleronlyhouse')
    house_total = request.form.get('house_total')
    house_org = request.form.get('house_org')
    house_area = request.form.get('house_area')
    house_year = request.form.get('house_year')
    # house_type = request.form.get('house_type')
    house_location = request.form.get('house_location')


    buyerfirsthouse = str(buyerfirsthouse)
    selleronlyhouse = str(selleronlyhouse)
    house_area = float(house_area)
    house_total = float(house_total) * 10000
    house_org = float(house_org) * 10000
    house_year = int(house_year)
    house_location = str(house_location)
    # 内环以内:0
    # 内外环之间:1
    # 外环仕外:2

    if house_area > 140:
        house_type = 'non_ordinary'
    else:
        if house_total < 4500000 and house_location == '0':
            house_type = 'ordinary'
        elif house_total < 3100000 and house_location == '1':
            house_type = 'ordinary'
        elif house_total < 2300000 and house_location == '2':
            house_type = 'ordinary'
        else:
            house_type = 'non_ordinary'

    # house_type = str(house_type)

    if buyerfirsthouse == 'on':
        buyerfirsthouse = '0'
    else:
        buyerfirsthouse = '1'

    if selleronlyhouse == 'on':
        selleronlyhouse = '0'
    else:
        selleronlyhouse = '1'

    print "buyerfirsthouse: " + str(buyerfirsthouse)
    print "selleronlyhouse: " + str(selleronlyhouse)
    print "house_area: " + str(house_area)
    print "house_total: " + str(house_total)
    print "house_org: " + str(house_org)
    print "house_year: " + str(house_year)
    print "house_type: " + str(house_type)
    print "house_location: " + str(house_location)
    # house_type:0 普通
    # buyerfirsthouse:0 买方唯一
    # selleronlyhouse:0 卖方唯一

    income_tax = personal_income_tax(house_type, house_year, house_total, house_org, selleronlyhouse)
    total_personal_income_tax = int(income_tax[0])
    margin_personal_income_tax = int(income_tax[1])
    total_vat = int(vat(house_type, house_year, house_total, house_org))
    deed_total = house_total - total_vat
    total_deed_tax = int(deed_tax(buyerfirsthouse, deed_total, house_area))

    # if total_personal_income_tax > margin_personal_income_tax:
    #     personal_tax = margin_personal_income_tax
    # else:
    #     personal_tax = total_personal_income_tax

    personal_tax = total_personal_income_tax

    seller_total = personal_tax + total_vat
    buyer_total = total_deed_tax

    print income_tax
    print total_personal_income_tax
    print margin_personal_income_tax
    print total_vat
    print total_deed_tax

    all_tax = seller_total + buyer_total



    return render_template('tax/tax_result.html', total_vat=total_vat, total_deed_tax=total_deed_tax,
                           seller_total=seller_total, buyer_total=buyer_total, all_tax=all_tax, personal_tax=personal_tax)


#个人所得税
def personal_income_tax(house_type, house_year, house_total, house_org, selleronlyhouse):

    income_tax = []

    if house_type == 'ordinary':
        if house_year == 5:
            if selleronlyhouse == '0':
                income_tax_reason = '普通满5年且卖方唯一住房，个人所得税为0'
                total_personal_income_tax = 0
                margin_personal_income_tax = 0
                print income_tax_reason
            else:
                income_tax_reason = '普通满5年但非卖方唯一住房，个人所得税为（房屋现总价-房屋原价）*20%, 或者 房屋现总价 * 0.01'
                total_personal_income_tax = house_total * 0.01
                margin_personal_income_tax = (house_total - house_org) * 0.2
                print income_tax_reason
        else:
            income_tax_reason = '普通不满5年，个人所得税为（房屋现总价-房屋原价）*20%, 或者 房屋现总价 * 0.01'
            total_personal_income_tax = house_total * 0.01
            margin_personal_income_tax = (house_total - house_org) * 0.2
            print income_tax_reason
    else:
        if house_year == 5:
            if selleronlyhouse == '0':
                income_tax_reason = '非普通满5年且卖方唯一住房，个人所得税为0'
                total_personal_income_tax = 0
                margin_personal_income_tax = 0
                print income_tax_reason
            else:
                income_tax_reason = '非普通满5年但非卖方唯一住房，个人所得税为（房屋现总价-房屋原价）*20%, 或者 房屋现总价 * 0.02'
                total_personal_income_tax = house_total * 0.02
                margin_personal_income_tax = (house_total - house_org) * 0.2
                print income_tax_reason
        else:
            income_tax_reason = '非普通房产证不满5年，个人所得税为（房屋现总价-房屋原价）*20%, 或者 房屋现总价 * 0.02'
            total_personal_income_tax = house_total * 0.02
            margin_personal_income_tax = (house_total - house_org) * 0.2
            print income_tax_reason

    income_tax.append(total_personal_income_tax)
    income_tax.append(margin_personal_income_tax)

    return income_tax



#卖方 增值税
#注：过去征税房价是含税价，营改增后是不含税价，税率维持5%不变，实际税收负担降为4.76%。
def vat(house_type, house_year, house_total, house_org):
    if house_type == 'ordinary':
        if house_year == 0:
            vat_reason = '普通住宅购房不满2年，增值税为总房价的5.6%'
            print vat_reason
            total_vat = house_total * 0.056 / 1.05
        else:
            vat_reason = '普通住宅购房满2年，增值税为0'
            print vat_reason
            total_vat = 0
    else:
        if house_year == 0:
            vat_reason = '非普通住宅购房不满2年，增值税为总房价的5.6%'
            print vat_reason
            total_vat = house_total * 0.056 / 1.05
        else:
            vat_reason = '非普通住宅购房满2年，增值税为（房屋现总价 - 房屋原价）* 5.6%'
            print vat_reason
            total_vat = (house_total - house_org ) * 0.056 / 1.05

    return total_vat


#买方交: 契税：
def deed_tax(buyerfirsthouse, house_total, house_area):

    if buyerfirsthouse == '0':
        if house_area > 90:
            deed_tax_reason = '首次购房且面积≤90㎡，契税为总房价的1%'
            total_deed_tax = house_total * 0.01
            print deed_tax_reason
        else:
            deed_tax_reason = '首次购房且>90㎡，契税为总房价的1.5%'
            total_deed_tax = house_total * 0.015
            print deed_tax_reason
    else:
        deed_tax_reason = '非首次购买，契税为总房价的3%'
        total_deed_tax = house_total * 0.03
        print deed_tax_reason

    return total_deed_tax



@tax.route('/tax', methods=['GET', 'POST'])
def tax():
    return render_template('tax/tax.html')



