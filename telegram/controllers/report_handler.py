from telegram.control import Handler, Control
from telebot import types
from order.models import OrderItem
from product.models import Product
import xlsxwriter
from django.db.models import Q
import os


class ReportHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, msg: types.Message, message_id=None):
        file = xlsxwriter.Workbook("report.xlsx")
        worksheet = file.add_worksheet("General report")

        header = file.add_format({
        })
        header.set_align('center')
        # header.set_bg_color("#C0C0C0")

        first_column = file.add_format({
            # 'bg_color': 'DCDCDC'
        })

        worksheet.activate()
        worksheet.set_column(0, 3, 15)
        worksheet.merge_range(0, 0, 0, 3, "General report", header)
        worksheet.write(1, 0, "Product", header)
        worksheet.write(1, 1, "Sales (sum)", header)
        worksheet.write(1, 2, "Amount", header)
        worksheet.write(1, 3, "Orders", header)
        products = Product.objects.all()
        row = 2
        for product in products:
            worksheet.write(row, 0, product.name_uz, first_column)
            order_items = product.order_items.order_by('order__created_at').filter(
                Q(order__status='accepted') | Q(order__status='paid'))

            sales_sum = 0
            amount = 0
            orders = 0
            for order_item in order_items:
                order_item: OrderItem
                sales_sum += order_item.amount * order_item.price
                amount += order_item.amount
                orders += 1

            worksheet.write(row, 1, sales_sum)
            worksheet.write(row, 2, amount)
            worksheet.write(row, 3, orders)
            row += 1

            product_worksheet = file.add_worksheet(f"{product.name_uz} report")
            product_worksheet.activate()
            product_worksheet.set_column(0, 3, 13)

            product_worksheet.merge_range(
                0, 0, 0, 3, f"Product report {product.name_uz}", header)
            for i, name in enumerate(["Customers", "Date", "Sales", "Amount"]):
                product_worksheet.write(1, i, name, header)
            product_row = 2

            for order_item in order_items:
                product_worksheet.write(
                    product_row, 0, order_item.order.user.phone, first_column)
                product_worksheet.write(
                    product_row, 1, order_item.order.created_at.strftime("%d.%m.%y"))
                product_worksheet.write(
                    product_row, 2, order_item.amount*order_item.price)
                product_worksheet.write(
                    product_row, 3, order_item.amount)
                product_row += 1
            worksheet.activate()

        file.close()

        file = open('report.xlsx', 'rb')
        self.control.bot.send_document(msg.chat.id, file)
        file.close()

        os.system("rm report.xlsx")
