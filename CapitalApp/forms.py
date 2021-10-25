from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField, DateField,
                     FloatField, SelectField)
from wtforms.validators import DataRequired, Length


class NewCreditForm(FlaskForm):
    name = StringField("Название кредита:", validators=[DataRequired()])
    date_start = DateField("Дата выдачи:", validators=[DataRequired()])
    total_month = IntegerField("Срок кредита, мес:", validators=[DataRequired(),
                                                                 Length(max=4)])
    percent = FloatField("Процент", validators=[DataRequired()])
    amount = FloatField("Сумма кредита", validators=[DataRequired()])
    amount_value = SelectField('Валюта', choices=[('RUB', 'RUB'),
                                                  ('USD', 'USD'),
                                                  ('EUR', 'EUR')],
                               validators=[DataRequired()])
    submit = SubmitField("")
