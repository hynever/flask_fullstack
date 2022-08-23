from .baseform import BaseForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import Email, InputRequired, Length


class AddStaffForm(BaseForm):
  email = StringField(validators=[Email(message="请输入正确格式的邮箱！")])
  role = IntegerField(validators=[InputRequired(message="请选择角色！")])


class EditStaffForm(BaseForm):
  is_staff = BooleanField(validators=[InputRequired(message="请选择是否为员工！")])
  role = IntegerField(validators=[InputRequired(message="请选择分组！")])


class EditBoardForm(BaseForm):
  board_id = IntegerField(validators=[InputRequired(message="请输入板块ID！")])
  name = StringField(validators=[Length(min=1,max=20,message="请输入1-20位长度！")])