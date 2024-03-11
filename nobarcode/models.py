from django.db import models




class Material(models.Model):
    name = models.TextField(verbose_name='Vật liệu', unique=True)

    def __str__(self):
        return self.name
    

class ProcessingStage(models.Model):
    process_name = models.CharField(max_length=255, verbose_name='Công đoạn')

    def __str__(self):
        return self.process_name

class Sno(models.Model):
    sno = models.TextField(verbose_name='S no', unique=True)

    def __str__(self):
        return self.sno

class ProcessingTime(models.Model):
    sno = models.ForeignKey(Sno, on_delete=models.CASCADE, related_name='processing_times', verbose_name='Mã số thiết bị')
    stt = models.IntegerField(verbose_name='Thứ tự công đoạn')
    stage = models.ForeignKey(ProcessingStage, on_delete=models.CASCADE, related_name='processing_times', verbose_name='Công đoạn')
    # time_required = models.FloatField(verbose_name='Thời gian gia công (phút)')
    time_required = models.IntegerField(verbose_name='Thời gian gia công (phút)')

    def __str__(self):
        return f"{self.sno} - {self.stage.process_name}"

class Order(models.Model):
    S_NO_CHOICES = [
        ('Có S chuẩn', 'Có S chuẩn'),
        ('Sẽ làm S chuẩn', 'Sẽ làm S chuẩn'),
        ('Không làm S chuẩn', 'Không làm S chuẩn'),
    ]

    sno = models.ForeignKey(Sno, on_delete=models.CASCADE, related_name='order', verbose_name='Mã số thiết bị')
    type_s = models.CharField(max_length=50, choices=S_NO_CHOICES, verbose_name='Loại S', null=True, blank=True)
    materials = models.TextField(verbose_name='Vật liệu')
    specification = models.CharField(max_length=255, verbose_name='Quy cách 1 pcs', null=True, blank=True)
    v1 = models.CharField(max_length=255, verbose_name='V1', null=True, blank=True)
    v2 = models.CharField(max_length=255, verbose_name='V2', null=True, blank=True)
    syc_skc = models.CharField(max_length=255, verbose_name='Số yêu cầu', null=True, blank=True)
    drawing = models.FileField(upload_to='order_drawings/', verbose_name='Bản vẽ PDF', blank=True, null=True)


    def __str__(self):
        return f"{self.sno} - {self.materials}"






class RequestInfo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='request_info', verbose_name='Mã số thiết bị')
    request_number = models.CharField(max_length=255, verbose_name='Số yêu cầu')
    rep_number = models.IntegerField(verbose_name='Số rep')
    quantity = models.IntegerField(verbose_name='Số lượng', null=True, blank=True)

    def __str__(self):
        return f'{self.request_number} - {self.rep_number}'

from django.contrib.auth.models import User

class StageTuchu(models.Model):
    requirement = models.ForeignKey(RequestInfo, on_delete=models.CASCADE)
    StageTuchu = models.CharField(max_length=255, verbose_name='Stage Tuchu')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Employee')
    stt = models.IntegerField(verbose_name='STT')

    def __str__(self):
        return f'{self.stt} - {self.StageTuchu} - {self.employee}'

class Inspection(models.Model):
    stage = models.ForeignKey(StageTuchu, on_delete=models.CASCADE, verbose_name='Stage')
    inspect = models.CharField(max_length=255, verbose_name='Inspection',null=True)
    max_value = models.FloatField(verbose_name='Max Value',null=True)
    min_value = models.FloatField(verbose_name='Min Value',null=True)
    ok_ng = models.CharField(max_length=5, verbose_name='OK/NG',null=True) 
    stt = models.IntegerField(verbose_name='STT')



    def __str__(self):
        return f'{self.stage} - {self.inspect}'


class RequestSttProcessing(models.Model):
    request_number = models.OneToOneField(RequestInfo, on_delete=models.CASCADE, primary_key=True)
    current_stt = models.IntegerField(verbose_name='Công đoạn hiện tại', default=1)

    def __str__(self):
        return f"{self.request_number} - {self.current_stt}"


class EmployeeProcessing(models.Model):
    request_info = models.ForeignKey(RequestInfo, on_delete=models.CASCADE, related_name='employee_processing', verbose_name='Số yêu cầu')
    sno = models.ForeignKey(Sno, on_delete=models.CASCADE, related_name='employee_processing', verbose_name='Mã số thiết bị')
    stt = models.IntegerField(verbose_name='Số thứ tự')
    stage = models.ForeignKey(ProcessingStage, on_delete=models.CASCADE, related_name='employee_processing', verbose_name='Công đoạn')
    execution_time = models.IntegerField(verbose_name='Thời gian gia công (phút)', default = 0)
    # execution_status = models.CharField(
    #     max_length=255, 
    #     choices=[
    #         ('pending', 'Pending'),
    #         ('in_progress', 'In Progress'),
    #         ('completed', 'Completed'),
    #     ],
    #     default='pending',
    #     verbose_name='Trạng thái thực thi'
    # )
    def __str__(self):
        return f"{self.request_info} - {self.stage.process_name}"

# class AdditionalExecution(models.Model):

from django.contrib.auth.models import User
class ExecutionTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='execution_times', verbose_name='User')
    shift = models.CharField(max_length=10)
    num_machine = models.CharField(max_length=10)
    employee_processing = models.ForeignKey(EmployeeProcessing, on_delete=models.CASCADE, related_name='execution_times', verbose_name='Employee Processing')
    time_start = models.DateTimeField(verbose_name='Start Time')
    time_end = models.DateTimeField(verbose_name='End Time')
    duration = models.IntegerField(verbose_name='Duration', default = 0)

    def __str__(self):
        return f"{self.user.username} - {self.employee_processing}"


class WorkDate(models.Model):

    ENO_CHOICES = [
        ('E100', 'E100'),
        ('E200', 'E200'),
        ('E300', 'E300'),
        ('E400', 'E400'),
        ('E500', 'E500'),
        ('E600', 'E600'),
        ('E700', 'E700'),
        ('E800', 'E800'),
        ('E900', 'E900'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_dates', verbose_name='User')
    date = models.DateField()
    shift = models.CharField(max_length=10)
    eno = models.CharField(max_length=20, choices=ENO_CHOICES, default='E100')
    time_start = models.TimeField()
    time_end = models.TimeField()
    duration_time = models.IntegerField()
    note = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.date} - {self.eno}"


class NameEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='name_employee', verbose_name='User')
    name = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.name}"
    
# class OrderMaterial(models.Model):
#     order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='order_material', verbose_name='Mã số thiết bị')
#     material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='order_materials', verbose_name='Vật liệu')

#     def __str__(self):
#         return f"{self.order.sno} - {self.material.name}"






# class Drawing(models.Model):
#     order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='drawing', verbose_name='Mã số thiết bị')
#     pdf = models.FileField(upload_to='order_drawings/', verbose_name='Bản vẽ PDF', blank=True, null=True)

#     def __str__(self):
#         return f"{self.order.sno} - Drawing"








# class Order(models.Model):
#     S_NO_CHOICES = [
#         ('Có S chuẩn', 'Có S chuẩn'),
#         ('Sẽ làm S chuẩn', 'Sẽ làm S chuẩn'),
#         ('Không làm S chuẩn', 'Không làm S chuẩn'),
#         # Add more choices as needed
#     ]

#     sno = models.CharField(max_length=255, verbose_name='Sno')
#     type_s = models.CharField(max_length=50, choices=S_NO_CHOICES, verbose_name='Loại S', null=True, blank=True)
#     specification = models.CharField(max_length=255, verbose_name='Quy cách 1 pcs', null=True, blank=True)

#     def __str__(self):
#         return self.sno





# models.py

# from django.db import models

# class Order(models.Model):
#     S_NO_CHOICES = [
#         ('Có S chuẩn', 'Có S chuẩn'),
#         ('Sẽ làm S chuẩn', 'Sẽ làm S chuẩn'),
#         ('Không làm S chuẩn', 'Không làm S chuẩn'),
#         # Add more choices as needed
#     ]

#     sno = models.CharField(max_length=255, verbose_name='Sno')
#     type_s = models.CharField(max_length=50, choices=S_NO_CHOICES, verbose_name='Loại S', null=True, blank=True)

#     def __str__(self):
#         return self.sno

# class Specification(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255, verbose_name='Quy cách 1 pcs')

#     def __str__(self):
#         return self.name



# from django.db import models

# class Specification(models.Model):
#     specification_text = models.CharField(max_length=255, verbose_name='Quy cách 1 pcs')

#     def __str__(self):
#         return self.specification_text

# class Order(models.Model):
#     S_NO_CHOICES = [
#         ('Có S chuẩn', 'Có S chuẩn'),
#         ('Sẽ làm S chuẩn', 'Sẽ làm S chuẩn'),
#         ('Không làm S chuẩn', 'Không làm S chuẩn'),
#         # Add more choices as needed
#     ]

#     sno = models.CharField(max_length=255, verbose_name='Sno')
#     type_s = models.CharField(max_length=50, choices=S_NO_CHOICES, verbose_name='Loại S', null=True, blank=True)
#     specifications = models.ManyToManyField(Specification, verbose_name='Quy cách 1 pcs', blank=True)

#     def __str__(self):
#         return self.sno


# from django.db import models

# class Order(models.Model):
#     S_NO_CHOICES = [
#         ('Có S chuẩn', 'Có S chuẩn'),
#         ('Sẽ làm S chuẩn', 'Sẽ làm S chuẩn'),
#         ('Không làm S chuẩn', 'Không làm S chuẩn'),
#         # Add more choices as needed
#     ]

#     id = models.AutoField(primary_key=True)
#     sno = models.CharField(max_length=255, verbose_name='Sno')
#     type_s = models.CharField(max_length=50, choices=S_NO_CHOICES, verbose_name='Loại S', null=True, blank=True)
#     specification = models.CharField(max_length=255, verbose_name='Quy cách 1 pcs', null=True, blank=True)

#     def __str__(self):
#         return self.sno




class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

