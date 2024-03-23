# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm

from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.contrib.auth import logout
from django.contrib import messages

from django.http import HttpResponse

import os

from django.shortcuts import render,get_object_or_404

from django.templatetags.static import static


from .forms import ExcelFileForm, RequestInfoForm
from .models import Order
import pandas as pd


from django.views import View
from .models import Order

from .models import Sno


from .models import Order, Sno

from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Order, Sno, ProcessingTime

from django.views.generic import DetailView
from .models import RequestInfo



from django.shortcuts import render, redirect
from django.views import View
from .models import RequestInfo

class EditRequestDetailView(View):
    template_name = 'edit_request_detail.html'

    def get(self, request, *args, **kwargs):
        request_info = RequestInfo.objects.get(pk=kwargs['pk']) 
        if request_info.rep_number !=0:
            instance = f'{request_info.order.sno}_{request_info.request_number}_{request_info.rep_number}'
        else:
            instance = f'{request_info.order.sno}_{request_info.request_number}'

        context = {
            'request_info': request_info,
            'instance':instance
        }
            
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        request_info = RequestInfo.objects.get(pk=kwargs['pk'])

        request_info.request_number = request.POST.get('request_number')
        request_info.rep_number = request.POST.get('rep_number')
        request_info.quantity = request.POST.get('quantity')

        request_info.drawing_type = request.POST.get('drawing_type')
        request_info.inspection = request.POST.get('inspection')
        request_info.make_black = request.POST.get('make_black')
        request_info.usually_or_urgent = request.POST.get('usually_or_urgent')



        request_info.save()
        return redirect('request_detail', pk=request_info.pk)



class RequestDetailView(DetailView):
    # model = RequestInfo
    template_name = 'request_detail.html'  
    # context_object_name = 'request_info'
    def get(self, request, *args, **kwargs):
        request_info = RequestInfo.objects.get(pk=kwargs['pk'])  

        sno_instance = request_info.order.sno 
        selected_order = Order.objects.filter(sno=sno_instance)
        if len(selected_order) >=2:
            materials = ''
            v2 = ''

            for sl in selected_order:
                try:
                    drawing = sl.drawing.url
                except:
                    drawing = None
                if sl != selected_order.last():
                    materials += sl.materials + ', '
                    v2 += sl.v2 + ', '
                else:
                    materials += sl.materials
                    v2 += sl.v2 



            context = {
                'request_info': request_info,
                'materials': materials,
                'v2': v2,
                'drawing':drawing
            }



            
        else:
   
            selected_order = Order.objects.filter(sno=sno_instance).first()
            materials = selected_order.materials
            v2 = selected_order.v2
            try:
                drawing = selected_order.drawing.url
            except:
                drawing = None

            context = {
                'request_info': request_info,
                'materials': materials,
                'v2': v2,
                'drawing':drawing

            }

            
        return render(request, self.template_name, context)

def delete_request(request, request_id):
    request_info = get_object_or_404(RequestInfo, id=request_id)
    
    if request.method == 'POST':
        # Xác nhận xóa và thực hiện xóa
        request_info.delete()
        return redirect('request_list')

    return render(request, 'delete_request.html', {'request_info': request_info})


class SnoEditDetailView(View):

    def get(self, request, sno=None, *args, **kwargs):

        drawing = None
  

        if sno.count('_') == 2:
            sno, request_number, so_rep = sno.split('_')
            instance_tail = f'_{request_number}_{so_rep}'

            sno_instance = get_object_or_404(Sno, sno=sno)
            
            selected_order = Order.objects.filter(sno=sno_instance, syc_skc = request_number, so_rep = int(so_rep))

            if not selected_order :
   
                selected_order = Order.objects.filter(sno=sno_instance)



        elif sno.count('_') == 1:
            sno, request_number = sno.split('_')

            instance_tail = f'_{request_number}'
        

            sno_instance = get_object_or_404(Sno, sno=sno)
            
            selected_order = Order.objects.filter(sno=sno_instance, syc_skc = request_number)
            if not selected_order:
                selected_order = Order.objects.filter(sno=sno_instance)

        else:
            sno_instance = get_object_or_404(Sno, sno=sno)
            
            selected_order = Order.objects.filter(sno=sno_instance)#.first()
            # so = selected_order.first()
            # try:
            #     request_info = RequestInfo.objects.get(order = so)
            #     instance_tail = f'_{request_info.request_number}_{request_info.rep_number}'
            # except:
            #     instance_tail = ''
            instance_tail = ''





        materials_all = Material.objects.all()

        # if len(selected_order) >=2:
        materials = []
        ahead_specifications = []
        specifications = []
        type_s = ''
  
        for sl in selected_order:

            type_s = sl.type_s
            try:
                drawing = sl.drawing.url
            except:
                drawing = None
            # if sl != selected_order.last():
            #     materials += sl.materials + ', '
            #     specification += sl.specification + ', '
            # else:
            #     materials += sl.materials
            #     specification += sl.specification 
            materials.append(sl.materials)
            ahead_specifications.append(sl.specification[0])
            specifications.append(sl.specification[1:])

        processing_times = ProcessingTime.objects.filter(sno=sno_instance)
        processing_stages = ProcessingStage.objects.all()

 
        if drawing is not None:
            context = {
                'instance_tail': instance_tail,
                'sno_instance': sno_instance,
                'type_s': type_s,
                'materials': materials_all,
                'form_data': zip(materials, ahead_specifications, specifications),
                'processing_stages':processing_stages,
                'processing_times': processing_times,
                'drawing':drawing

            }
        else:
            context = {
                'instance_tail': instance_tail,
                'sno_instance': sno_instance,
                'type_s': type_s,
                'materials': materials_all,
                'form_data': zip(materials, ahead_specifications, specifications),
                'processing_stages':processing_stages,
                'processing_times': processing_times,


            }     

        # return render(request, 'sno_material.html', context)
        return render(request, 'sno_detail_edit2.html', context)


            
        # else:
        #     # Get the ProcessingTime instances related to the Sno
        #     selected_order = Order.objects.filter(sno=sno_instance).first()

        #     processing_times = ProcessingTime.objects.filter(sno=sno_instance)

        #     context = {
        #         'sno_instance': sno_instance,
        #         'selected_order': selected_order,
        #         'processing_times': processing_times,
        #     }

        #     return render(request, 'sno_detail_edit.html', context)




class SnoDetailView(View):

    def get(self, request, sno=None, *args, **kwargs):
        # Get the Sno instance
        instance = sno
        if sno.count('_') == 2:

            sno, request_number, so_rep = sno.split('_')
            # instance_tail = f'_{request_number}_{so_rep}'

            sno_instance = get_object_or_404(Sno, sno=sno)
            selected_order = Order.objects.filter(sno=sno_instance, syc_skc = request_number, so_rep = so_rep)

        elif sno.count('_') == 1:
            
            sno, request_number = sno.split('_')
            # instance_tail = f'_{request_number}'

            sno_instance = get_object_or_404(Sno, sno=sno)
            selected_order = Order.objects.filter(sno=sno_instance, syc_skc = request_number)

        else:
            # instance_tail = ''
            sno_instance = get_object_or_404(Sno, sno=sno)
            selected_order = Order.objects.filter(sno=sno_instance)#.first()
        if len(selected_order) >=2:
            materials = ''
            specification = ''
            type_s = ''
            for sl in selected_order:
                try:
                    drawing = sl.drawing.url
                except:
                    drawing = None
                type_s = sl.type_s
                if sl != selected_order.last():
                    materials += sl.materials + ', '
                    specification += sl.specification + ', '
                else:
                    materials += sl.materials
                    specification += sl.specification 

            processing_times = ProcessingTime.objects.filter(sno=sno_instance)
            # processing_stages = ProcessingStage.objects.all()

            context = {
                'instance': instance,
                'type_s': type_s,
                'materials': materials,
                'specification': specification,
                # 'processing_stages':processing_stages,
                'processing_times': processing_times,
                'drawing': drawing

            }

            # return render(request, 'sno_material.html', context)
            return render(request, 'sno_detail2.html', context)


            
        else:
            # Get the ProcessingTime instances related to the Sno
            selected_order = Order.objects.filter(sno=sno_instance).first()
            try:
                drawing = selected_order.drawing.url
            except:
                drawing = None
            processing_times = ProcessingTime.objects.filter(sno=sno_instance)

            context = {
                'instance': instance,
                'selected_order': selected_order,
                'processing_times': processing_times,
                'drawing': drawing
            }

            return render(request, 'sno_detail.html', context)


class SnoDetailView2(View):

    def get(self, request, sno=None, material=None, *args, **kwargs):
        # Get the Sno instance
        sno_instance = get_object_or_404(Sno, sno=sno)

        # Get the associated Order instance
        selected_order = Order.objects.filter(sno=sno_instance,materials=material).first()

        processing_times = ProcessingTime.objects.filter(sno=sno_instance)

        context = {
            'sno_instance': sno_instance,
            'selected_order': selected_order,
            'processing_times': processing_times,
        }

        return render(request, 'sno_detail.html', context)


def sno_detail(request, sno):
    sno_instance = get_object_or_404(Sno, sno=sno)
    processing_times = ProcessingTime.objects.filter(sno=sno_instance)

    context = {
        'sno_instance': sno_instance,
        'processing_times': processing_times,
    }

    return render(request, 'sno_detail.html', context)


class ClearOrderView(View):
    template_name = 'clear_order.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Xóa tất cả dữ liệu trong model Order
        Order.objects.all().delete()

        # Redirect đến trang hiển thị kết quả
        return redirect('clear_order_result')

class ClearOrderResultView(View):
    template_name = 'clear_order_result.html'  # Sửa tên template

    def get(self, request, *args, **kwargs):


        return render(request, self.template_name)



from django.shortcuts import render, redirect
from django.views import View
from .models import Order, Sno

class ClearSnoView(View):
    template_name = 'clear_sno.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Xóa tất cả dữ liệu trong model Sno
        Sno.objects.all().delete()

        # Redirect đến trang hiển thị kết quả
        return redirect('clear_sno_result')

class ClearSnoResultView(View):
    template_name = 'clear_sno_result.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)


class ClearProcessingTimeView(View):
    template_name = 'clear_processingtime.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Xóa tất cả dữ liệu trong model Sno
        ProcessingTime.objects.all().delete()

        # Redirect đến trang hiển thị kết quả
        return redirect('clear_processingtime_result')

class ClearProcessingTimeResultView(View):
    template_name = 'clear_processingtime_result.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)


from django.db.models import Q
from .models import Material, ProcessingStage, ProcessingTime, Order, RequestInfo, Sno

def import_data_from_excel(file_path):
    file_name = os.path.basename(file_path)

    if file_name.startswith("Sno"):
        df = pd.read_excel(file_path)
        sno_list = []

        def snos_equal(sno1, sno2):
            return sno1.sno == sno2.sno

        for _, row in df.iterrows():
            new_sno = Sno(
                sno=row['sno']
            )

            duplicate_found = any(snos_equal(new_sno, existing_sno) for existing_sno in sno_list)

            if not duplicate_found:
                sno_list.append(new_sno)

        Sno.objects.bulk_create(sno_list)

    if file_name.startswith("Order"):
        df = pd.read_excel(file_path)
        orders_list = []

        # Hàm kiểm tra xem hai đối tượng Order có giá trị giống nhau hay không
        def orders_equal(order1, order2):
            return (
                order1.sno == order2.sno and
                order1.type_s == order2.type_s and
                order1.materials == order2.materials and
                order1.specification == order2.specification
            )

        for _, row in df.iterrows():
            try:
                sno = Sno.objects.get(sno=row['sno'])

                new_order = Order(
                    sno=sno,
                    type_s=row['type_s'],
                    materials=row['materials'],
                    specification=row['specification'],

                )

                duplicate_found = any(orders_equal(new_order, existing_order) for existing_order in orders_list)

                if not duplicate_found:
                    orders_list.append(new_order)
            except:
                pass

        Order.objects.bulk_create(orders_list)

    if file_name.startswith("Material"):
        df = pd.read_excel(file_path)
        materials_list = []

        for _, row in df.iterrows():
            existing_material = Material.objects.filter(
                name=row['name']
            ).first()

            if not existing_material:
                new_material = Material(
                    name=row['name']
                )
                materials_list.append(new_material)

        unique_materials_list = []
        seen_material_names = set()

        for material in materials_list:
            if material.name not in seen_material_names:
                unique_materials_list.append(material)
                seen_material_names.add(material.name)

        Material.objects.bulk_create(unique_materials_list)

    if file_name.startswith("ProcessingStage"):
        df = pd.read_excel(file_path)
        processing_stages_list = []

        for _, row in df.iterrows():
            existing_processing_stage = ProcessingStage.objects.filter(
                process_name=row['process_name']
            ).first()

            if not existing_processing_stage:
                new_processing_stage = ProcessingStage(
                    process_name=row['process_name']
                )
                processing_stages_list.append(new_processing_stage)

        unique_processing_stages_list = []
        seen_processing_stages_names = set()

        for processing_stages in processing_stages_list:
            if processing_stages.process_name not in seen_processing_stages_names:
                unique_processing_stages_list.append(processing_stages)
                seen_processing_stages_names.add(processing_stages.process_name)


        ProcessingStage.objects.bulk_create(unique_processing_stages_list)

    if file_name.startswith("ProcessingTime"):
        df = pd.read_excel(file_path)
        processing_times_list = []

        def processing_times_equal(processing_time1, processing_time2):
            return (
                processing_time1.sno == processing_time2.sno and
                processing_time1.stage == processing_time2.stage and
                processing_time1.stt == processing_time2.stt and
                processing_time1.time_required == processing_time2.time_required
            )

        for _, row in df.iterrows():
            try:
                sno = Sno.objects.get(sno=row['sno'])
                stage = ProcessingStage.objects.get(process_name=row['stage'])

                new_processing_time = ProcessingTime(
                    sno=sno,
                    stt=row['stt'],
                    stage=stage,
                    time_required=row['time_required']
                )

                duplicate_found = any(processing_times_equal(new_processing_time, existing_processing_time) for existing_processing_time in processing_times_list)

                if not duplicate_found:
                    processing_times_list.append(new_processing_time)
            except:
                pass

        ProcessingTime.objects.bulk_create(processing_times_list)

    if file_name.startswith("RequestInfo"):
        df = pd.read_excel(file_path)
        request_info_list = []

        for _, row in df.iterrows():
            order_sno = row['order_sno']

            order = Order.objects.get(sno=order_sno)

            existing_request_info = RequestInfo.objects.filter(
                order=order,
                request_number=row['request_number'],
                quantity=row['quantity']
            ).first()

            if not existing_request_info:
                new_request_info = RequestInfo(
                    order=order,
                    request_number=row['request_number'],
                    quantity=row['quantity']
                )
                request_info_list.append(new_request_info)

        unique_request_info_list = []
        seen_request_info_names = set()

        for request_info in request_info_list:
            if request_info.name not in seen_request_info_names:
                unique_request_info_list.append(request_info)
                seen_request_info_names.add(request_info.name)

        RequestInfo.objects.bulk_create(unique_request_info_list)

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.save()
            file_path = excel_file.file.path
            import_data_from_excel(file_path)
            return HttpResponse("Data imported successfully!")
    else:
        form = ExcelFileForm()

    return render(request, 'upload_excel.html', {'form': form})




def pdf_view(request):
    pdf_path = static('sample.pdf')
    return render(request, 'pdf_view.html', {'pdf_path': pdf_path})



# def view_pdf(request):
#     pdf_path = "D:/ckv2/cokhi/media/sample.pdf"  # Đặt đường dẫn đến tệp PDF của bạn ở đây
#     return render(request, 'pdf_view.html', {'pdf_path': pdf_path})






from django.shortcuts import render
from .models import Order



def home(request):
    choose_types = [
        ('Có S chuẩn', 'Có S chuẩn'),
        ('Sẽ làm S chuẩn', 'Sẽ làm S chuẩn'),
        ('Không làm S chuẩn', 'Không làm S chuẩn'),
        # Add more choices as needed
    ]

    context = {
        'choose_types': choose_types,
    }

    return render(request, 'home.html', context)



from django.shortcuts import render, get_object_or_404

from .models import Order

# def order_detail(request, order_id):
#     selected_order = get_object_or_404(Order, id=order_id)
#     return render(request, 'order_detail.html', {'order': selected_order})

# def sno_list(request, order_type_s):
#     # Assuming sno is a unique identifier for orders
#     # orders = Order.objects.all()
#     if order_type_s == '1':
#         selected_types = 'Có S chuẩn'
#         context = {'types':selected_types}
#         all_sno = Sno.objects.all()
#         context['all_sno'] = all_sno


#     elif order_type_s == '2':
#         selected_types = 'Sẽ làm S chuẩn'    
#         context = {'types':selected_types}

#     elif order_type_s == '3':
#         selected_types = 'Không làm S chuẩn'
#         context = {'types':selected_types}
def sno_list(request):
    selected_types = 'Có S chuẩn'
    context = {'types':selected_types}
    # all_sno = Sno.objects.all()

    # Lấy vị trí của order_type_s trong S_NO_CHOICES
    # all_sno = []
    # selected_orders = Order.objects.filter(type_s=selected_types)
    # for so in selected_orders:
    #     all_sno.append(so.sno)
    selected_orders = Order.objects.filter(type_s=selected_types)
    # all_sno = selected_orders.values_list('sno__sno', flat=True)
    all_sno = list(set(selected_orders.values_list('sno__sno', flat=True)))
    

    context['all_sno'] = all_sno


    return render(request, 'sno_list.html', context)

def sno_kochuan_list(request):
    selected_types = 'Không làm S chuẩn'
    context = {'types':selected_types}

    # selected_orders = Order.objects.filter(type_s=selected_types)
    selected_orders = Order.objects.filter(type_s=selected_types)

    # all_sno = selected_orders.values_list('sno__sno', flat=True)
    # all_sno = list(set(selected_orders.values_list('sno__sno', flat=True)))
    # all_sno = [f"{order.sno.sno}_{order.syc_skc}_{order.so_rep}" if order.syc_skc is not None and order.sorep != 0 elif  else f"{order.sno.sno}" for order in selected_orders]
    
    all_sno = [
        f"{order.sno.sno}_{order.syc_skc}_{order.so_rep}" 
        if order.syc_skc is not None and order.so_rep != 0 and order.so_rep is not None
        else f"{order.sno.sno}_{order.syc_skc}" 
        if order.syc_skc is not None and (order.so_rep == 0 or order.so_rep is None)
        else f"{order.sno.sno}"
        for order in selected_orders
    ]
    all_sno = list(set(all_sno))

    context['all_sno'] = all_sno


    return render(request, 'sno_list.html', context)



def order_detail(request, order_sno):
    selected_order = get_object_or_404(Order, sno=order_sno)
    pdf_path =  selected_order.drawing.pdf.url 

    pdf_path = static(pdf_path)

    return render(request, 'order_detail.html', {'order': selected_order,'pdf_path':pdf_path})

from django.shortcuts import render
from .models import Order  # Đảm bảo bạn đã import model Order hoặc thay thế bằng tên model thích hợp



# def order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     return render(request, 'order_detail.html', {'order': order})


# # Create your views here.
# def home(request):
#     pdf_path = static('a.pdf')
#     # return render(request, 'pdf_view.html', {'pdf_path': pdf_path})
#     return render(request, "home.html", {'pdf_path': pdf_path})


import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def a(request):

    materials = Material.objects.all()

    context = {'materials': materials}
    return render(request, "b.html",context)


# views.py
@csrf_exempt
def post_test(request):
    if request.method == 'POST':

        table_data_json = request.body.decode('utf-8')
        table_data = json.loads(table_data_json)
        table_data = table_data.get('tableData', [])

        for row in table_data:
            stt = row.get('stt', '')
            congdoan_name = row.get('congdoan_name', '')
            thoigian = row.get('thoigian', '')



# @csrf_exempt
# def post_order(request):
#     if request.method == 'POST':
#         sno = request.POST.get('selected_order_sno')
#         request_number = request.POST.get('so_yeu_cau')
#         quantity = request.POST.get('so_luong')
#         type_s = request.POST.get('loai_s_chuan')
#         materials = request.POST.get('selected_material')
#         specification = request.POST.get('hiddenQuyCach')
#         drawing = request.POST.get('pdf_path', '')

#         table_data_json = request.body.decode('utf-8')
#         table_data = json.loads(table_data_json)
#         table_data = table_data.get('tableData', [])

#         for row in table_data:
#             stt = row.get('stt', '')
#             stage = row.get('congdoan_name', '')
#             time_required = row.get('thoigian', '')
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from pathlib import Path
import shutil
def post_order(request):

    if request.method == 'POST':

        csrf_token = request.POST.get('csrfmiddlewaretoken', '')
        request_number_value = request.POST.get('tableData[0][soYeuCau]', '')
        quantity_value = request.POST.get('tableData[0][soLuong]', '')
        rep_value = request.POST.get('tableData[0][soRep]', '')
        type_s_value = request.POST.get('tableData[0][loaiSChuan]', '')
        sno_value = request.POST.get('tableData[0][sNo]', '')
        loaibanve_value = request.POST.get('tableData[0][loaiBanVe]', '')
        kiemtra_value = request.POST.get('tableData[0][kiemTra]', '')
        lamden_value = request.POST.get('tableData[0][lamDen]', '')
        thuonggap_value = request.POST.get('tableData[0][thuongGap]', '')

        drawing_file_old = request.POST.get('tableData[0][pdf_path]', '')
 


        if drawing_file_old != '':

            drawing_file = drawing_file_old.replace("temp", "order_drawings")   
             

            base_dir = Path(__file__).resolve().parent.parent
            drawing_file_old_absolute = os.path.join(base_dir, drawing_file_old.lstrip('/'))
            drawing_file_absolute = os.path.join(base_dir, drawing_file.lstrip('/'))

            shutil.copy(drawing_file_old_absolute, drawing_file_absolute)

        if type_s_value == 'Sẽ làm S chuẩn':
            type_s_value = 'Có S chuẩn'

        sno_object, created = Sno.objects.get_or_create(sno=sno_value)

        
        from django.db.models import Q
        for i in range(1, len(request.POST)):
            if request.POST.get(f'tableData[{i}][vatlieu]', '') != '':
                materials_value = request.POST.get(f'tableData[{i}][vatlieu]', '')
                specification_value = request.POST.get(f'tableData[{i}][quycach]', '')
                v1_value = request.POST.get(f'tableData[{i}][v1]', '')
                v2_value = request.POST.get(f'tableData[{i}][v2]', '')


                order_object = Order.objects.filter(
                    Q(sno=sno_object) & Q(materials=materials_value)
                ).first()

                if order_object is None:
                    if drawing_file_old != '':
                        drawing_file = drawing_file.replace("/static/media/", "")  
                        order_object = Order.objects.create(
                            sno=sno_object,
                            type_s=type_s_value,
                            materials=materials_value,
                            specification=specification_value,
                            v1 = v1_value,
                            v2 = v2_value,
                            syc_skc = request_number_value,
                            so_rep = rep_value,
                            drawing=drawing_file
                        )
                    else:
                        order_object = Order.objects.create(
                            sno=sno_object,
                            type_s=type_s_value,
                            materials=materials_value,
                            specification=specification_value,
                            v1 = v1_value,
                            v2 = v2_value,
                            syc_skc = request_number_value,
                            so_rep = rep_value,

                            # drawing=drawing_file
                        )



                try:
                    request_info_object = RequestInfo.objects.get(request_number=request_number_value,rep_number = rep_value)

                except RequestInfo.DoesNotExist:
                    request_info_object = RequestInfo.objects.create(
                        order=order_object,
                        request_number=request_number_value,
                        rep_number = rep_value,
                        quantity=quantity_value,
                        drawing_type = loaibanve_value,
                        inspection = kiemtra_value,
                        make_black = lamden_value,
                        usually_or_urgent = thuonggap_value
                    )
                    sno_object, created = Sno.objects.get_or_create(sno=sno_value)
                    RequestSttProcessing.objects.create(request_number=request_info_object)




        for i in range(1, len(request.POST) // 3 -1):
            if request.POST.get(f'tableData[{i}][stt]', '') != '':
                stt_value = request.POST.get(f'tableData[{i}][stt]', '')
                stage_name_value = request.POST.get(f'tableData[{i}][congdoan_name]', '')
                time_required_value = request.POST.get(f'tableData[{i}][thoigian]', '')


                stage_object, created = ProcessingStage.objects.get_or_create(process_name=stage_name_value)

                try:
                    processing_time_object = ProcessingTime.objects.get(sno=sno_object, stt=stt_value)
                except ProcessingTime.DoesNotExist:
                    processing_time_object = ProcessingTime.objects.create(
                        sno=sno_object,
                        stt=stt_value,
                        stage=stage_object,
                        time_required=time_required_value
                    )

                EmployeeProcessing.objects.get_or_create(
                    request_info=request_info_object,
                    sno=sno_object,
                    stt=processing_time_object.stt,
                    stage=processing_time_object.stage,
                    execution_time=0
                )

        response_data = {
            'success': True,
            'redirect_url': reverse('request_list')
        }

        return JsonResponse(response_data)


from django.http import HttpResponse
from django.conf import settings
import os



from urllib.request import urlretrieve
def sno_detail_edit_save(request):

    if request.method == 'POST':


        if 'pdfFile' in request.FILES:
            pdf_file = request.FILES['pdfFile']

            base_dir = Path(__file__).resolve().parent.parent
            
            file_path = str(base_dir) + '/static/media/order_drawings/' + pdf_file.name

            
            with default_storage.open(file_path, 'wb+') as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)

        csrf_token = request.POST.get('csrfmiddlewaretoken', '')
        type_s_value = request.POST.get('tableData[0][loaiSChuan]', '')
        sno_old_value = request.POST.get('tableData[0][snoOldValue]', '')

        sno_value = request.POST.get('tableData[0][sNo]', '')
        instance_value = request.POST.get('tableData[0][instance]', '')

        if instance_value.count('_') ==2:
            _,syc_skc, so_rep = instance_value.split('_')
        elif instance_value.count('_') ==1:
            _,syc_skc = instance_value.split('_')
            so_rep = None
        else:
            syc_skc = None
            so_rep = None


        drawing_file_old = request.POST.get('tableData[0][pdf_path]', '')

        iframe_value = request.POST.get('tableData[0][iframe_value]', '')
        pdfFile = request.FILES.get('tableData[0][formData]', '')

        if instance_value:

            sno_object, created = Sno.objects.get_or_create(sno=sno_value)

            if not created and sno_value != sno_old_value:
                response_data = {
                    'success': False,
                    'inform': f'Giá trị sno {sno_value} đã được sử dụng'
                }

                return JsonResponse(response_data)  

            else:  
                sno_old = Sno.objects.get(sno=sno_old_value)
                # if syc_skc is not None:
                #     try:
    
                #         my_order =  Order.objects.get(sno =sno_old, type_s = type_s_value, syc_skc = syc_skc, so_rep = so_rep)
                #         request_info  = RequestInfo.objects.get(order=my_order,request_number = syc_skc, rep_number =so_rep)
                #         quantity_value =  request_info.quantity

                #     except:

                # my_order =  Order.objects.get(sno =sno_old, type_s = type_s_value)

                my_order =  Order.objects.filter(sno =sno_old, type_s = type_s_value).first()

                request_infos  = RequestInfo.objects.filter(order=my_order)#,request_number = syc_skc, rep_number =so_rep)
                list_ri = []

                
                for request_info in request_infos:
       
                    request_number_value = request_info.request_number
                    rep_number_value = request_info.rep_number
                    quantity_value = request_info.quantity
                    drawing_type_value  = request_info.drawing_type
                    inspection_value = request_info.inspection
                    make_black_value = request_info.make_black
                    usually_or_urgent_value = request_info.usually_or_urgent


                    list_ri.append([request_number_value,rep_number_value,quantity_value,drawing_type_value,inspection_value,make_black_value,usually_or_urgent_value])

                list_pt = []
                processing_times = ProcessingTime.objects.filter(sno=sno_old)
                for processing_time in processing_times:
                    list_pt.append([processing_time.stt, processing_time.stage, processing_time.time_required])


                        # quantity_value =  request_info.quantity
                # else:
                #     my_order =  Order.objects.get(sno =sno_old, type_s = type_s_value)
                #     request_info  = RequestInfo.objects.filter(order=my_order)
                #     quantity_value =  request_info.quantity                
                # request_infos.delete()
                sno_old.delete()
                if not created:
                    sno_object = Sno.objects.create(sno=sno_value)
                # from django.db.models import Q
                for i in range(1, len(request.POST)):
                    if request.POST.get(f'tableData[{i}][vatlieu]', '') != '':
                        materials_value = request.POST.get(f'tableData[{i}][vatlieu]', '')
                        specification_value = request.POST.get(f'tableData[{i}][quycach]', '')
                        drawing_file_save = drawing_file_old.strip().replace('/media/', '')

                        if drawing_file_old != '':
                            order_object = Order.objects.create(
                                sno=sno_object,
                                type_s=type_s_value,
                                materials=materials_value,
                                specification=specification_value,
                                syc_skc = syc_skc,
                                so_rep = so_rep,
                                drawing=drawing_file_save
                            )
                        else:
                            order_object = Order.objects.create(
                                sno=sno_object,
                                type_s=type_s_value,
                                materials=materials_value,
                                specification=specification_value,
                                syc_skc = syc_skc,
                                so_rep = so_rep,
                                # drawing=drawing_file
                            )


                for ri in list_ri:

                    request_info_object = RequestInfo.objects.create(
                        order=order_object,
                        request_number=ri[0],
                        rep_number = ri[1],
                        quantity=ri[2],
                        drawing_type = ri[3],
                        inspection = ri[4],
                        make_black = ri[5],
                        usually_or_urgent = ri[6]
                    )
                    RequestSttProcessing.objects.create(request_number=request_info_object)

                    
                    
                    for pt in list_pt:
                        processing_time_object = ProcessingTime.objects.get_or_create(
                            sno=sno_object,
                            stt=pt[0],
                            stage=pt[1],
                            time_required=pt[2]
                        )

                        EmployeeProcessing.objects.get_or_create(
                            request_info=request_info_object,
                            sno=sno_object,
                            stt=pt[0],
                            stage=pt[1],
                            execution_time=0
                        )

                for i in range(1, len(request.POST) // 3 -1):
                    if request.POST.get(f'tableData[{i}][stt]', '') != '':
                        stt_value = request.POST.get(f'tableData[{i}][stt]', '')
                        stage_name_value = request.POST.get(f'tableData[{i}][congdoan_name]', '')
                        time_required_value = request.POST.get(f'tableData[{i}][thoigian]', '')
                        print(stt_value, ' ',stage_name_value ,' ',time_required_value)

                        stage_object, created = ProcessingStage.objects.get_or_create(process_name=stage_name_value)

                        processing_time_object = ProcessingTime.objects.create(
                            sno=sno_object,
                            stt=stt_value,
                            stage=stage_object,
                            time_required=time_required_value
                        )

                redirect_url = reverse('sno_detail', kwargs={'sno': instance_value})
                
                response_data = {'success': True, 'redirect_url': redirect_url}

                return JsonResponse(response_data)
        else:
            return redirect('home')



from .models import Material,ProcessingStage
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.templatetags.static import static
from .models import ExecutionTime, EmployeeProcessing
# def nhanvien(request):
#     materials = Material.objects.all()
#     processingStages = ProcessingStage.objects.all()
#     context = {'materials': materials, 'loop_times': range(1, 100), 'processingStages': processingStages}
#     pdf_path = ''

#     if request.method == 'POST':
#         if request.FILES.get('pdfFile'):
#             pdf_file = request.FILES['pdfFile']
#             file_path = f'temp/{pdf_file.name}'

#             with default_storage.open(file_path, 'wb') as destination:
#                 for chunk in pdf_file.chunks():
#                     destination.write(chunk)
#             file_path = 'media/' + file_path
#             pdf_path = static(file_path)
#     context['pdf_path'] = pdf_path  

#     return render(request, "thietlap.html", context)



def thietlap(request):
    request_numbers = list(RequestInfo.objects.values_list('request_number', flat=True))
    request_numbers_json = json.dumps(request_numbers)
    context = {'request_numbers_json': request_numbers_json}
    return render(request, "thietlap.html", context)

def giacong(request):
    all_request_info = RequestInfo.objects.all()
    return render(request, 'giacong.html', {'all_request_info': all_request_info})

def thongtingiacong(request):
    all_request_info = RequestInfo.objects.all()
    return render(request, 'thongtingiacong.html', {'all_request_info': all_request_info})


from .models import EmployeeProcessing
def soyeucau_detail(request, request_number):
    rep_number = 0 
    c_request_number = request_number
    if "-" in request_number:
        request_and_rep = request_number.split('-')
        request_number = request_and_rep[0].strip()
        rep_number = request_and_rep[1].strip()


    request_info = get_object_or_404(RequestInfo, request_number=request_number, rep_number = rep_number)
    
    sno_instance = request_info.order.sno


    selected_order = Order.objects.filter(sno=sno_instance)

    if len(selected_order) >=2:
        materials = ''
        specification = ''

        for sl in selected_order:
            try:
                drawing = sl.drawing.url
            except:
                drawing = None
            if sl != selected_order.last():
                materials += sl.materials + ', '
                specification += sl.specification + ', '
            else:
                materials += sl.materials
                specification += sl.specification 

    else:
        selected_order = Order.objects.filter(sno=sno_instance).first()
        try:
            drawing = selected_order.drawing.url
        except:
            drawing = None
        materials = selected_order.materials
        specification = selected_order.specification




    
    processing_instances = EmployeeProcessing.objects.filter(request_info=request_info, sno=sno_instance)

    execution_times = ExecutionTime.objects.filter(employee_processing__in=processing_instances).order_by('-pk')

    list_stage = []
    list_ex = []
    for ex in execution_times:
        if ex.employee_processing.stage not in list_stage:
            list_stage.append(ex.employee_processing.stage)
            list_ex.append(ex)


    list_pi_st = [pi.stage.process_name for pi in processing_instances]
    list_ls_st = [str(ls) for ls in list_stage]
    st_remain = list(set(list_pi_st) - set(list_ls_st))


    len_processing_instances = len(processing_instances)
    request_stt_processing_instance = RequestSttProcessing.objects.get(request_number=request_info)

    current_stt_value = request_stt_processing_instance.current_stt
    already_finish = 0 
    for ex in execution_times:
        if ex.employee_processing.stt == current_stt_value:
            already_finish = 1 

            print('đã có nhấn kết thúc')




    if request.method == 'POST' and request.POST.get('minutes') is not None:
        shift = request.POST.get('shift')
        num_machine = request.POST.get('num_machine')
        minutes = request.POST.get('minutes')
        time_start = request.POST.get('time_start')
        time_end = request.POST.get('time_end')

        processing_current = EmployeeProcessing.objects.get(request_info=request_info, sno=sno_instance, stt = current_stt_value)
        processing_current.execution_time += int(minutes)
        processing_current.save()

        execution_time = ExecutionTime.objects.create(
            user=request.user,  
            shift = shift,
            num_machine = num_machine,
            employee_processing=processing_current,
            time_start=time_start,
            time_end=time_end,
            duration = minutes
        )
        response_data = {
            'success': True, 
            'redirect_url': reverse('tuchu_detail', kwargs={'request_number': c_request_number}),
        }
        return JsonResponse(response_data)


    if request.method == 'POST' and request.POST.get('hoantat') is not None:
        request_stt_processing_instance.current_stt +=1
        if request_stt_processing_instance.current_stt > len_processing_instances:
            request_stt_processing_instance.current_stt = 0
        request_stt_processing_instance.save()
        current_stt_value = request_stt_processing_instance.current_stt

        context = {
            'request_info': request_info,
            'processing_instances': processing_instances,
            'current_stt_value':current_stt_value
        }

        # return render(request, 'soyeucau_detail.html', context)
        response_data = {'success': True}
        return render(request, 'soyeucau_detail.html', context) and JsonResponse(response_data)

    context = {
        'request_info': request_info,
        'drawing':drawing,
        'processing_instances': processing_instances,
        'list_ex': list_ex,
        'st_remain':st_remain,
        'current_stt_value':current_stt_value,
        'already_finish':already_finish
    }

    return render(request, 'soyeucau_detail.html', context)



from .models import WorkDate
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def baocaohoatdong(request):
    eno_choices = WorkDate.ENO_CHOICES
    current_user = request.user
    user_instance = User.objects.get(username=current_user)
    name_employee = NameEmployee.objects.get(user=user_instance)

    full_name = name_employee.name
    context = {'eno_choices': eno_choices}
    context['current_user'] = current_user
    context['full_name'] = full_name
    ca_lam_viec = ['A','B','C','D','E','F']
    context['ca_lam_viec'] = ca_lam_viec
    
    worksdate = WorkDate.objects.filter(user=user_instance, date=timezone.now().date())
    if worksdate.exists():
        context['worksdate']= worksdate

    return render(request, 'baocaohoatdong.html', context)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
@csrf_exempt
def save_baocaohoatdong(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rows_data = data.get('data', [])
        work_dates = []
        if rows_data != []:
            current_user = rows_data[0].get('current_user', '')
            user = User.objects.get(username=current_user)
            shift = rows_data[0].get('selectedCa', '')

            worksdate = WorkDate.objects.filter(user=user, date=timezone.now().date())
            if worksdate.exists():
                worksdate.delete()
            for row_data in rows_data:
                eno = row_data.get('input1', '')
                eno = eno.strip().replace('\n', ' ')
                time_start = row_data.get('input2', '')
                time_start = time_start.strip().replace('\n', ' ')
                time_end = row_data.get('input3', '')
                time_end = time_end.strip().replace('\n', ' ')
                duration_time = row_data.get('input4', '')
                duration_time = int(str(duration_time).strip().replace('\n', ' '))
                # duration_time = timedelta(minutes=int(duration_time))
                note = row_data.get('input5', '')
                note = note.strip().replace('\n', ' ')



                work_date = WorkDate(
                    user=user,
                    date=timezone.now().date(),
                    shift=shift,
                    eno=eno,
                    time_start=time_start,
                    time_end=time_end,
                    duration_time=duration_time,
                    note=note
                )

                work_dates.append(work_date)

            with transaction.atomic():
                WorkDate.objects.bulk_create(work_dates)

            response_data = {
                'success': True,
                'redirect_url': reverse('baocaohoatdong'),
            }


            return JsonResponse(response_data)



        return JsonResponse({'success': False})


def giacong_detail(request, request_number):
    rep_number = 0 
    if "-" in request_number:
        request_and_rep = request_number.split('-')
        request_number = request_and_rep[0].strip()
        rep_number = request_and_rep[1].strip()

    request_info = get_object_or_404(RequestInfo, request_number=request_number, rep_number = rep_number)
    execution_times = ExecutionTime.objects.filter(employee_processing__request_info=request_info)

    employee_processing_unused = EmployeeProcessing.objects.filter(request_info=request_info).exclude(
        id__in=ExecutionTime.objects.filter(employee_processing__request_info=request_info).values_list('employee_processing__id', flat=True)
    )



    employee_processing_instances = execution_times.values('employee_processing__id').distinct()
    employee_processing_list = [
        {
            'employee_processing': ExecutionTime.objects.filter(employee_processing_id=instance['employee_processing__id']).first().employee_processing,
            'execution_times': ExecutionTime.objects.filter(employee_processing_id=instance['employee_processing__id'])
        }
        for instance in employee_processing_instances
    ]

    context = {'request_info': request_info, 'employee_processing_list': employee_processing_list,'employee_processing_unused': employee_processing_unused}
    return render(request, 'giacong_detail.html', context)


def thietlap_sno(request):


    if request.method == 'POST':
        so_yeu_cau = request.POST.get('so_yeu_cau')
        so_luong = request.POST.get('so_luong')
        so_rep = request.POST.get('so_rep') 
        loai_s_chuan = request.POST.get('loai_s_chuan')
        if loai_s_chuan is not None:
            if loai_s_chuan != 'Không làm S chuẩn':
                s_take = 'Có S chuẩn'
            else:
                s_take = 'Không làm S chuẩn'

            orders = Order.objects.filter(type_s=s_take)

            all_sno = list(set(orders.values_list('sno__sno', flat=True)))

            context = {'all_sno':all_sno, 'orders': orders,'so_yeu_cau': so_yeu_cau,'so_rep':so_rep ,'so_luong': so_luong,'so_rep':so_rep,'loai_s_chuan': loai_s_chuan}
            return render(request, "thietlap_sno.html", context)


        # if loai_s_chuan == 'Có S chuẩn':

        #     # all_sno = Sno.objects.all()
        #     orders = Order.objects.filter(type_s=loai_s_chuan)
        #     # all_sno = orders.values_list('sno__sno', flat=True)
        #     all_sno = list(set(orders.values_list('sno__sno', flat=True)))

                
        #     context = {'all_sno':all_sno, 'orders': orders,'so_yeu_cau': so_yeu_cau,'so_rep':so_rep ,'so_luong': so_luong,'so_rep':so_rep,'loai_s_chuan': loai_s_chuan}

        #     return render(request, "thietlap_sno.html", context)
        
        # if loai_s_chuan == 'Sẽ làm S chuẩn':
        #     context = {'so_yeu_cau': so_yeu_cau, 'so_luong': so_luong,'so_rep':so_rep, 'loai_s_chuan': loai_s_chuan}
        #     return render(request, "thietlap_sno.html", context)

        # if loai_s_chuan == 'Không làm S chuẩn':
        #     context = {'so_yeu_cau': so_yeu_cau, 'so_luong': so_luong,'so_rep':so_rep, 'loai_s_chuan': loai_s_chuan}
        #     return render(request, "thietlap_sno.html", context)

    return render(request, "thietlap_sno.html")


# def thietlap_material(request):
#     materials = None
#     # specification = None
#     # processing_times = None

#     if request.method == 'POST':
#         s_no = request.POST.get('selected_order_sno')
#         so_yeu_cau = request.POST.get('so_yeu_cau')
#         so_luong = request.POST.get('so_luong')
#         loai_s_chuan = request.POST.get('loai_s_chuan') 
#         vat_lieu = request.POST.get('selected_order_material')
#         sno_object = get_object_or_404(Sno, sno=s_no)

#         order_objects = Order.objects.filter(sno=sno_object, type_s=loai_s_chuan, materials = vat_lieu)
#         # Case 2: Single Order object
#         order_object = order_objects.first() 

#         if order_object:

#             materials = order_object.materials
#             # specification = order_object.specification
#             # processing_times = ProcessingTime.objects.filter(sno=sno_object)

#         context = {'s_no': s_no, 'so_yeu_cau': so_yeu_cau, 'so_luong': so_luong, 'loai_s_chuan': loai_s_chuan,
#                     'materials': materials} #, 'specification': specification, 'processing_times': processing_times}

#         return render(request, "thietlap_material.html", context)


from .models import RequestInfo, RequestSttProcessing

def request_list(request):
    request_infos = RequestInfo.objects.all()
    return render(request, 'request_list.html', {'request_infos': request_infos})


def b(request):
    materials = Material.objects.all()
    context = {'materials':materials}
    return render(request, "b.html", context)



def thietlap_detail(request):
    materials = None
    specification = None
    processing_times = None


    if request.method == 'POST':
        s_no = request.POST.get('selected_order_sno')
        so_yeu_cau = request.POST.get('so_yeu_cau')
        so_luong = request.POST.get('so_luong')
        so_rep = request.POST.get('so_rep')
        loai_s_chuan = request.POST.get('loai_s_chuan')
        vat_lieu = request.POST.get('selected_material')
        quy_cach_1_bit = request.POST.get('selected_specification')
        have_input_pdf = request.POST.get('have_input_pdf')

        loai_ban_ve = request.POST.get('loai_ban_ve')
        kiem_tra = request.POST.get('kiem_tra')
        lam_den = request.POST.get('lam_den')
        thuong_gap = request.POST.get('thuong_gap')


        if loai_s_chuan == 'Có S chuẩn':
            if vat_lieu is None and quy_cach_1_bit is None:
                sno_object = get_object_or_404(Sno, sno=s_no)

                order_objects = Order.objects.filter(sno=sno_object, type_s=loai_s_chuan)
                if len(order_objects) >=2:
                    # materials_list = []
                    # for order_object in order_objects:
                    #     materials_list.append(order_object.materials)

                    # materials = materials_list


                    materials = ''
                    specification = ''

                    for sl in order_objects:
                        try:
                            drawing = sl.drawing.url
                        except:
                            drawing = None
                        if sl != order_objects.last():
                            materials += sl.materials + ','
                            specification += sl.specification + ','
                        else:
                            materials += sl.materials
                            specification += sl.specification 

                    processing_times = ProcessingTime.objects.filter(sno=sno_object)

                    context = {'s_no': s_no, 'so_yeu_cau': so_yeu_cau, 'so_luong': so_luong,'so_rep':so_rep,'loai_s_chuan': loai_s_chuan,
                                'materials': materials, 'specification':specification,'drawing':drawing,'processing_times': processing_times}
                    

                    # return render(request, "thietlap_material.html", context)
                    return render(request, "thietlap_detail2.html", context)
                


                else:
                    # Case 2: Single Order object
                    order_object = order_objects.first() 

                    if order_object:

                        materials = order_object.materials
                        specification = order_object.specification
                        try:
                            drawing = order_object.drawing.url
                        except:
                            drawing = None
                        processing_times = ProcessingTime.objects.filter(sno=sno_object)

                    context = {'s_no': s_no, 'so_yeu_cau': so_yeu_cau, 'so_luong': so_luong,'so_rep':so_rep,'loai_s_chuan': loai_s_chuan,
                                'materials': materials, 'specification': specification, 'drawing':drawing, 'processing_times': processing_times}

                    return render(request, "thietlap_detail.html", context)

            # elif vat_lieu is not None and quy_cach_1_bit is None:

            #     sno_object = get_object_or_404(Sno, sno=s_no)

            #     order_objects = Order.objects.filter(sno=sno_object, type_s=loai_s_chuan, materials = vat_lieu)

            #     order_object = order_objects.first() 

            #     if order_object:

            #         materials = order_object.materials
            #         specification = order_object.specification
            #         processing_times = ProcessingTime.objects.filter(sno=sno_object)



            #     context = {'s_no': s_no, 'so_yeu_cau': so_yeu_cau, 'so_luong': so_luong, 'loai_s_chuan': loai_s_chuan,
            #                 'materials': materials, 'specification': specification, 'processing_times': processing_times}
                
            #     return render(request, "thietlap_detail.html", context)
            
            elif vat_lieu is not None and quy_cach_1_bit is not None:
                
                order = Order.objects.filter(sno__sno=s_no,type_s=loai_s_chuan).first()
                
                existing_request_info = RequestInfo.objects.filter(request_number=so_yeu_cau).first()

                if existing_request_info:
                    messages.warning(request, f'Số yêu cầu {so_yeu_cau} đã tồn tại.')

                else:
                    request_info = RequestInfo.objects.create(
                        order=order, request_number=so_yeu_cau, rep_number=so_rep, quantity=so_luong,
                        drawing_type =loai_ban_ve,inspection =kiem_tra, make_black=lam_den, usually_or_urgent=thuong_gap)
                    RequestSttProcessing.objects.create(request_number=request_info)


                    sno_object = get_object_or_404(Sno, sno=s_no)
                    processing_times = ProcessingTime.objects.filter(sno=sno_object)
                    for processing_time in processing_times:
                        EmployeeProcessing.objects.create(
                            request_info=request_info,
                            sno=sno_object,
                            stt=processing_time.stt,
                            stage=processing_time.stage,
                            execution_time=0  
                        )


                    messages.success(request, f'Số yêu cầu {so_yeu_cau} đã được thêm thành công.')


                return redirect('request_list')


        if loai_s_chuan == 'Sẽ làm S chuẩn' or loai_s_chuan == 'Không làm S chuẩn':
            materials = Material.objects.all()
            # materials = ['1','2','3']


            processing_stages = ProcessingStage.objects.all()



            context = {'s_no': s_no,'so_yeu_cau': so_yeu_cau, 'so_luong': so_luong,'so_rep':so_rep, 'loai_s_chuan': loai_s_chuan,'materials': materials}
            # return render(request, "thietlap_text_material.html", context)

            pdf_path = ''
            # if request.method == 'POST' and request.FILES.get('pdfFile'):
            if request.method == 'POST' and have_input_pdf == 'have_input_pdf':

                s_no = request.POST.get('selected_order_sno')
                so_yeu_cau = request.POST.get('so_yeu_cau')
                so_luong = request.POST.get('so_luong')
                so_rep = request.POST.get('so_rep')
                loai_s_chuan = request.POST.get('loai_s_chuan')
                # vat_lieu = request.POST.get('selected_material')
                quy_cach_1_bit = request.POST.get('selected_specification')
                # context = {'s_no': s_no,'so_yeu_cau': so_yeu_cau, 'so_luong': so_luong, 'loai_s_chuan': loai_s_chuan,'vat_lieu': vat_lieu}

                context = {'s_no': s_no,'so_yeu_cau': so_yeu_cau, 'so_luong': so_luong,'so_rep':so_rep, 'loai_s_chuan': loai_s_chuan,'materials': materials,'processing_stages':processing_stages}
                dict_material_stages = {'TRUC': ['abcd', 'P3.17X95', 'P2X62', 'P2.3X77'], 'SUS': ['T2X1200X2000', 'T1.5X800X1200', 'T3X800X1200', 'T1.5X1200X2000', 'T2X800X1200', 'T1X800X1200', 'T1X1200X2000', 'P25X1000', 'T25X300X500', 
                    'T12X300X500', 'T1.2X800X1200', 'T20X300X500', 'P85X500', 'P80X500', 'P30X1000', 'P22X1000', 'T32X300X500', 'T22X300X500', 'P55X500', 'P45X500', 'T4X300X500', 'P90X500', 'P16X1000', 'P75X500', 'P28X1000', 'P12X1000', 'P14X1000', 'P20X1000', 'P32X1000', 'T16X300X500', 'T0.7X800X1200', 'T0.6X800X1200', 'P101.6XP93.6X10', 'P50X500', 'P7X1000', 'T0.3X800X1200', 'T0.4X800X1200', 'P10X1000', 'T0.2X800X1200', 'T0.1X800X1200', 'P8X1000', 'P6X1000', 'T0.5X800X1200', 'T5X300X500', 'P5X1000', 'P1.8X160', 'T6X300X500', 'T40X300X500', 'T10X300X500', 'T8X300X500'], 'SKD11': ['T130X305X500', 'T85X305X500', 'T38X300X500', 'T32X300X500', 'T22X300X500', 'P132X500', 'P75X500', 'P90X500', 'P95X500', 'P110X500', 'P20X1000', 'T8X300X500', 'T70X300X500', 'P55X500', 'P25X1000', 'T5X205X1000', 'P120X500', 
                    'P70X500', 'T4X205X1000', 'P42X500', 'T50X300X500', 'P85X500', 'P12X1000', 'T25X300X500', 'P7X1000', 'P9X1000', 'P8X1000', 'P22X1000', 'P5X1000', 'T3X205X1000', 'T6X205X1000', 'P4X1000', 'P10X1000', 'P3X1000', 'P6X1000', 'P16X1000', 'P60X500', 'P50X500', 'P80X500', 'T20X300X500', 'P30X1000', 'P36X500', 'P65X500', 'T16X300X500', 'T13X300X500'], 'S45C': ['P50X500', 'T14X300X500', 'T60X300X500', 
                    'T22X300X500', 'T65X300X500', 'P150X500', 'T55X300X500', 'P95X500', 'P25X1000', 'P36X500', 'P90X500', 'P22X1000', 'T2X300X500', 'P60X500', 'P115X500', 'P70X500', 'T1X300X500', 'P55X500', 'P80X500', 
                    'T3X300X500', 'T46X300X500', 'P100X500', 'P18X1000', 'P28X1000', 'P35X500', 'P32X1000', 'P14X1000', 'P75X500', 'P42X500', 'P12X1000', 'P6X1000', 'T10 RETURN', 'P16X1000', 'P27X1000', 'P130X500', 'P13X1000', 'P10X1000', 'P46X500', 'T50X300X500', 'T28X300X500', 'T32X300X500', 'T26X300X500', 'P40X500', 'P30X1000', 'P85X500', 'T36X300X500', 'T40X300X500', 'P65X500', 'P20X1000', 'T30X300X500', 'T5X300X500', 'T16X300X500', 'T20X300X500', 'T12X300X500', 'T8X300X500', 'T10X300X500'], 'A606P': ['T12X500X500', 'T10X500X500', 'T8X500X500'], 'G04': ['T53X300X500', 'T60X300X500', 'P120X500', 'P85X500', 'T13X300X500', 'P50X500', 'T16X300X500', 'P46X500', 'P70X500', 'T25X300X500', 'P55X500', 'P19X1000', 'T19X300X500', 'P110X500', 'T32X300X500', 'P80X500', 'P32X500', 'P28X1000', 'P60X500', 'P16X1000', 'P36X500', 'P75X500', 'P65X500', 'P42X500', 'P13X1000', 'P22X1000', 'P90X500'], 'A6061': ['T10X800X1200', 'T15X500X500', 'T20X500X500', 'P30X1000', 'T6X500X500', 'P25X1000', 'T12X500X500', 'T40X300X500', 'T16X300X500', 'T10X500X500', 'T60X300X500', 'T25X300X500', 'P100X500', 'T3X500X500', 'P80X500', 'T50X300X500', 'T30X300X500', 'P65X500', 'P15X1000', 'P20X1000', 'P75X500', 'P55X500', 'P90X500', 'P40X500', 'P26X1000', 'T8X500X500', 'P130X500', 'P10X1000', 'T5X500X500'], 'C1720': ['P21X1000', 'P40X500', 'T25X300X500', 'T10X300X500', 'P15X1000 MASSKI', 'P15X1000 CHAU K', 'P25X1000', 'P22X1000', 'T16X300X500', 'P30X1000', 'P10X1000', 'P20X1000', 'P12X1000', 'T0.6X200X1000', 'P55X500', 'P1.2X1000', 'P6X1000', 'P1X1000', 'T20X300X500', 'P7X1000', 'P5X1000', 'P0.8X2000', 'P16X1000', 'P4X1000', 'T0.5X200X300', 'P8X1000', 'T0.7X200X500', 'T0.8X200X500', 'P46X500'], 'SK-3': ['T50X300X500', 'T32X300X500', 'T38X300X500', 'T25X305X500', 'P75X500', 'P100X500', 'T13X300X500', 'P90X500', 'T25X300X500', 'T22X300X500', 'P42X500', 'P65X500', 'P25X1000', 'P55X500', 'P60X500', 'P28X1000', 'P85X500', 'P32X500', 'P36X500', 'P22X1000', 'P30X1000', 'P19X1000', 'P6X1000', 'P38X500', 'P16X1000', 'T16X300X500', 'P50X500'], 'NAK55': ['T50X300X500', 'T70X300X500', 'T43X300X500', 'P80X500', 'P110X500', 'T38X300X500', 'T38X305X500', 'T16X305X500', 'P22X1000', 'T19X300X500', 'P75X500', 'P65X500', 'T32X300X500', 'P46X500', 'T22X300X500', 'T27X300X500', 'P19X1000', 'P42X500', 'P25X1000', 'P55X500', 'P16X1000', 'P13X1000', 'T13X300X500', 'P32X500'], 'BTP': ['S165842', 'S419961', 'S469311', 'S769867', 'S419966', 'EF05 10.5X20.5X', 'EF10 10.5X20.5X', 'REA25 10.5X20.5', 'REA35 10.5X20.5', 'RF06 10.5X20.5X', 'RF10 10.5X20.5X', 'S723723', 'S469900', 'R124607', 'R015901(EM10)', 'S901675', 'S842750', 'S783754', 'S820358', 'S914640', 'S831739', 'S083733', 'S896300', 'S620526', 'S163761', 'S159054', 'S823481', 'S733114', 'S913362', 'S083508', 'S083236', 'S797266', 'R105776', 'S056252', 'S901737', 'R058155', 'S766567', 'S056253', 'S898834', 'R028175', 'R028214', 'R032425', 'S001846', 'S156666', 'S902329', 'S933608', 'S941278', 'R056125', 'R110492', 'R337024', 'S163146', 'S935131', 'R058336', 'R069615', 'S212034', 'S251058', 'S262809', 'S856536', 'S770260', 'R069741', 'S083499', 'S903203', 'S161392', 'S903268', 'S087480', 'EF20 10.5X20.5X', 'R417935', 'S875030', 'R027917', 'R027962', 'R028119', 'R029029', 'R029060', 'R029061', 'R029085', 'R029159', 'R029321', 'R029340', 'R029403', 'R029475', 'R054992', 'R058132', 'R063145', 'R078247', 'R104394', 'R104406', 'R104415', 'R116090', 'R116173', 'R116787', 'R116789', 'R333469', 'R359400', 'R366819', 'S073929', 'S073930', 'S073937', 'S083695', 'S157020', 'S160710', 'S163763', 'S206235', 'S439279', 'S764009', 'S764013', 'S782960', 'S791872', 'S792792', 'S796625', 'S831752', 'S856488', 'S868339', 'S870521', 'S896299', 'S919916', 'S919918', 'S927142', 'S934912', 'S946965', 'S087724', 'S883064', 'S156670', 'R057995', 'R058015', 'R103504', 'R105763', 'R105773', 'S083735', 'S083740', 'S210894', 'S245251', 'S245335', 'S439169', 'S648245', 'S821855', 'S856500', 'S856518', 'S870520', 'S875947', 'S877340', 'S934868', 'R058275', 'R069123', 'S212037', 'S297473', 'S434416', 'S777347', 'S856556', 'S946963', 'S799056', 'PRD9N T10.5X20.', 'R007162-->R0367', 'R028959', 'R028973', 'R063055', 'R063140', 'R099763', 'R105768', 'R116537', 'R116539', 'R174874', 'R302351', 'R408125', 'R408127', 'R408147', 'R408519', 'R408524', 'R408525', 'R408546', 'R408549', 'R408557', 'R408558', 'R408691', 'R408697', 'R417887', 'R417900', 'R417903', 'R417904', 'R417920', 'R417937', 'R417952', 'R417961', 'R417973', 'R417979', 'R417988', 'R417989', 'R476103', 'R492813', 'R492859', 'S027890', 'S065486-->S4413', 'S073947', 'S723802<>S74221', 'S787211', 'S868326-S902329', 'S868361-->R3334', 'S870525', 'S885188', 'S899373', 'S916195', 'S919927', 'S934709', 'S935147', 'S948801', 'R003082', 'R008180', 'R008899', 'R009247', 'R027932', 'R027937', 'R027939', 'R027968', 'R027985', 'R027996', 'R028041', 'R028042', 'R028139', 'R028222', 'R029004', 'R029037', 'R029038', 'R029073', 'R029086', 'R029111', 'R030608', 'R036772', 'R058134', 'R058136', 'R058137', 'R058139', 'R058140', 'R058142', 'R058274', 'R058331', 'R063017', 'R063131', 'R063143', 'R066503', 'R071369', 'R071371', 'R095386', 'R101175', 'R101449', 'R103506', 'R103514', 'R103537', 'R104421', 'R104982', 'R105679', 'R105683', 'R105684', 'R105688', 'R105696', 'R105755', 'R105760', 'R105777', 'R106196', 'R116221', 'R116310', 'R116335', 'R116338', 'R116340', 'R152939', 'R171294', 'R181237', 'R181238', 'R181844', 'R333470', 'R360106', 'R360136', 'R366240', 'R366818', 'R369892', 'S005503', 'S019604', 'S027157', 'S028871', 'S031825', 'S033535', 'S034306', 'S069141', 'S073954', 'S077634', 'S083239', 'S083539', 'S083734', 'S083752', 'S101041', 'S101044', 'S101052', 'S101167', 'S154368', 'S156672', 'S156673', 'S157018', 'S157019', 'S157542', 'S157543', 'S157558', 'S158110', 'S163764', 'S163950', 'S206214', 'S206840', 'S209822', 'S210883', 'S245197', 'S422181', 'S432699', 'S434206', 'S439416', 'S441385', 'S473896', 'S473899', 'S609444', 'S628464', 'S648308', 'S759798', 'S774064', 'S780381', 'S780382', 'S785191', 'S785194', 'S786092', 'S786128', 'S788328', 'S790183', 'S790195', 'S792796', 'S796621', 'S796822', 'S796843', 'S797000', 'S831753', 'S837261', 'S850500', 'S857719', 'S861819', 'S867505', 'S870534', 'S870614', 'S870616', 'S883091', 'S883721', 'S883729', 'S895721', 'S895722', 'S903267', 'S911415', 'S911429', 'S911519', 'S911521', 'S933430', 'S933610', 'S935777', 'S936006', 'S936007', 'S941309', 'S945611', 'S945617', 'S946962', 'R015644', 'R029199', 'R029239', 'R058144', 'R058153', 'R058154', 'R103957', 'R104914', 'R105709', 'R105759', 'R105767', 'R116521', 'S027933', 'S030920', 'S157557', 'S163150', 'S455883', 'S842748', 'S870447', 'S895726', 'S903204', 'S941285', 'S029283', 'R049827', 'DKIF362A-00-1-0', 'S932877', 'S932882', 
                    'S921105', 'S617456', 'S411679', 'S443804', 'R058145', 'R066496', 'S934990', 'R007317', 'R027959', 'R028140', 'R028171', 'R053260', 'R058346', 'R066493', 'R066494', 'R066501', 'R066502', 'R066504', 
                    'R115892', 'R359402', 'R360105', 'R417918', 'S648316', 'S836079', 'S857331', 'S927141', 'S935146', 'R029167', 'R103539', 'R116776', 'R129856', 'S770313', 'S833627', 'R000569', 'S762923', 'R104420', 
                    'S034904(EM10)', 'R448186', 'S411658', 'S797928', 'S875016', 'S056860(EM10)'], 'POM': ['T10X500X500', 'T40X300X500', 'T6X500X1000', 'T12X500X500', 'T15X500X500', 'T5X500X1000', 'P130X500', 'T30X300X500', 'T50X300X500', 'T20X500X500', 'P30X1000', 'P90X500', 'P15X1000', 'P70X500', 'P25X1000', 'T35X300X500', 'P40X1000', 'T25X500X500', 'P45X500', 'P10X1000', 'P12.5X1000', 'P50X500', 'P8X1000', 'P20X1000'], 'SGTF': ['T50X305X500'], 'ACR-T': ['T15X1220X2440', 'T8X1220X2440', 'T3X1220X2440', 'T5X1220X2440', 'T10X1220X2440', 'T2X1220X2440', 'P40XP36X1000', 'T10X1220X2440BL'], 'C1100': ['T30X300X500', 'T40X300X500', 'T15X300X500', 'T20X300X500', 'P14X1000', 'P30X1000', 'P25X1000', 'P18X1000', 'P12X1000', 'T0.1X300X500', 'P8X1000', 'P10X1000', 'P3X2000', 'P6X1000', 'P20X1000', 'T10X300X500', 'P40X500', 'P16X1000'], 'SKS3': ['P55X500', 'P85X500', 'P120X500', 'P75X500', 'P95X500', 'P90X500', 'T4X305X1000', 'P70X500', 'P80X500', 'T60X300X500', 'T38X305X500', 'P42X500', 'P60X500', 'P25X1000', 'P46X500', 'P65X500', 'T5X205X1000', 'T6X205X1000', 'P22X1000', 'P36X500', 'P30X1000', 'P16X1000', 'T50X305X500', 'T8X305X1000', 'P50X500', 'P32X500', 'T16X305X500', 'T10X305X500', 'T19X305X500', 'T130X305X500', 'T32X305X500', 'T25X305X500', 'T13X305X500'], 'A7075': ['T70X300X500'], 'BS': ['T40X300X500', 'P20X1000', 'P16X1000', 'P50X500', 'T15X300X500', 'T20X300X500', 'T8X300X500', 'T45X300X500', 'P30X1000', 'T10X300X500', 'P75X500', 'T12X300X500', 'P55X500', 'P40X500', 'P85X500', 'P25X1000', 'T2X300X500', 'P8X1000', 'P6X1000', 'P10X1000', 'P4X1000'], 'CU-W': ['P20X200', 'P25X200', 'P45X200', 'P70X200', 'P35X200', 'P18X200', 'P14X200', 'P16X200', 'T15X50X100', 'P30X200', 'P12X200', 'P80X200', 'P6X200', 'P8X200', 'P10X200', 'P4X200', 'P60X200', 'P5X200', 'P2X150', 'P2.5X200', 'P3X200', 'T20X50X100', 'T25X50X100'], 'SLD': ['T32X320X500', 'T27X180X320'], 'SKH51': ['T30X200X300', 'P6X2000', 'P10X2000', 'P4.25X2000', 'P5X150', 'T20X50X100', 'P5.3X2000', 'P8X1000', 'P3.5X2000', 'P7.3X2000', 'P4X150', 'P3.4X2000', 'P3.1X2000', 'P3.2X2000', 'P2.5X2000', 'P2X2000', 'P2.4X2000', 'P1.8X2000', 'P2.9X1000', 'P3.2X200', 'P1.6X2000', 'P2.1X2000', 'P3.04X100', 'P3X2000', 'P6.3X2000'], 'MO': ['P6X200', 'P5X500', 'P5X196', 'P6X500', 'P3X160', 'P6X50'], 'C5191': ['P70X500', 'T30X200X200', 'T20X200X300', 'T5X180X1200', 'T15X200X300', 'P20X500', 'P0.8X2000', 'P1X2000'], 'ANP79': ['T10X300X500', 'T20X300X500', 'T11X300X500', 'T60X300X500', 'T15X300X500'], 'SGTR': ['P70X500'], 'SCM44': ['T55X300X500'], 'BAKEL': ['T6X800X1200', 'T25X800X1200', 'T20X800X1200', 'T8X800X1200', 'T50X300X500', 'T15X800X1200', 'P90X500', 'T10X800X1200', 'T35X300X500', 'P35X500', 'P45X500', 'P40X500', 'P60X500', 'P50X500', 'T30X300X500', 'P5X1000', 'P32X500', 'P25X1000', 'P20X1000', 'P16X1000', 
                    'T5X800X1200'], 'YWP': ['P5X200', 'P2X200', 'P3X200', 'T3.6X26X100', 'T6X26X100'], 'SLDR': ['P95X500', 'P55X500', 'P65X500'], 'SKD61': ['T13X300X500', 'T25X190X210', 'T19X190X210'], 'ASP23': ['P90X500', 'T43X210X300', 'P60X500', 'P14X500', 'P20X500', 'P80X500', 'T10X150X200'], 'FRP': ['T6X500X500', 'T8X300X300', 'T5X500X500', 'T3X300X500'], 'ELMAX': ['T32X200X500'], 'POMBL': ['T25X500X1000', 'T15X500X1000', 'T10X300X1000', 'T5X300X1000'], 'SKH9': ['T28X310X500', 'P6X1000'], 'SUYB1': ['P20X1000', 'P60X500'], 'SUS42': ['T25X300X300', 'T10X300X300', 'P14X1000'], 'SKS2': ['T3X305X1000', 'P8X1000', 'P13X1000', 'P7X1000', 'P9X1000', 'P12X1000', 'P3X1000', 'P4X1000', 'P5X1000', 'P6X1000', 'P10X1000', 'P20X1000', 'T6X205X1000'], 'RIGOR': ['T18X166X500', 'T22X166X500', 'T22X210X500', 'P15X1000', 'T32X210X500'], 'HPM1': ['P50X1000', 'P42X1000', 'T23X300X500'], 'WOOD': ['T5X245X245LAYTT', 'T6X245X245LAYTT'], 'ASP60': ['T23X210X300'], 'PEEK': ['P28X1000', 'P25X1000', 'T10X200X300', 'P50X500', 'P40X1000', 'T16X200X300', 'T20X150X250', 'T8X200X300', 'P30X1000'], 'SCM43': ['P45X500', 'P6X1250'], 'SLDMG': ['T10X150X200', 'T26X305X500', 'T23X300X500'], 'SUJ-2': ['P40X500', 'P12X1000', 'P65X500', 'P38X500', 'P32X500', 'P4X1000', 'P16X1000', 'P13X1000', 'P10X1000', 'P22X1000', 'P32X1000'], 'PANE': ['T0.7X102X1000', 'T0.9X102X1000', 'T0.2X102X1000', 'T0.6X102X1000', 'T0.8X102X1000', 
                    'T0.4X102X1000', 'T0.3X102X1000', 'T1.0X102X1000', 'T0.5X102X1000', 'T0.1X102X1000', 'T1.2X102X1000'], 'WCD30': ['T40X50X120', 'T26X50X120', 'T30X60X120', 'T24X50X100', 'T23X80X100', 'T13X65X130', 'T16X60X120', 'T6X50X100', 'T27X65X130', 'T25X50X100', 'P28X100', 'P30X100', 'T20X50X100', 'T9X65X100', 'P18X100', 'T16X50X100', 'P25X100', 'T22X50X100', 'P10X70', 'T16X80X100', 'P12X65', 'T9X50X100', 'P4X90', 'P7X80', 'P10X65', 'P5X60', 'P4X60', 'P4X50', 'P9X70', 'P5X100', 'P20X100', 'T23X50X120', 'P3.1X50', 'P12X100', 'P8X70', 'P3.1X65', 'P30X60', 'P22X100', 'P14X100', 'P7X70', 'T26X33X120', 
                    'T14X65X130', 'P7X55', 'T30X50X100', 'P6X70', 'P32X100', 'P26X100', 'T7X50X100', 'T18X50X100', 'T12X65X105'], 'WCD40': ['T23X70X75', 'T23X55X120', 'T22X55X120', 'T22X50X120', 'T11X70X100', 'P22X60', 'P30X75', 'P19X65', 'T20X50X100', 'P17X65', 'P4X65', 'P12X40', 'P12X60', 'P10X60', 'P5X65', 'P6X80', 'P7X50', 'P3X50', 'P6X60'], 'STAVA': ['T23X200X200'], 'C3604': ['P7X1000', 'T2X300X500', 'P10X1000', 'P13X1000', 'P8X1000'], 'SEIDO': ['P50X500', 'T10X210X300', 'P30X500'], 'VANAD': ['T10X150X200'], 'WCD25': ['T26X50X100', 'P28X100', 'P32X100', 'T22X50X100', 'P15X100', 'T9X50X100', 'P18X100', 
                    'P9X60', 'P7X60', 'P8X60', 'P10X60', 'P22X120'], 'WCV50': ['T9X50X100', 'T12X55X100', 'T6X50X100', 'T7X55X120', 'P9X70', 'T11X55X120', 'T10X55X120'], 'ASP30': ['T27X200X300'], 'MC901': ['T45X300X500'], 'WKD40': ['T16X50X100', 'T20X50X100', 'T7X50X100', 'T8X50X100', 'T9X50X100', 'T5X50X100', 'P5X60', 'P6X70', 'P10X60', 'P7X70'], 'ORESU': ['T11X105X1000', 'T8X105X1000', 'T13X105X1000', 'P7X500'], 'TEFLO': ['P8X1000', 'T10X300X500', 'P10X1000', 'P12X1000'], 'PHIP': ['P20X1000', 'T10X1000X1200', 'P3X1000', 'P16X1000'], 'SUS44': ['P22X500', 'T25X100X200'], 'CRCU': ['P8X1000', 'P6X1000', 'P5X1000'], 'WCD20': ['T20X50X100', 'T24X60X120', 'P9X100', 'T22X60X120', 'P20X60', 'P11X80', 'P21X60', 'P22X60', 'T9X60X120', 'T11X60X120', 'P6X70'], 'OILES': ['P36SX36#600', 'P36MX26#600'], 'PB2': ['P13X1000'], 'SUM24': ['P7X1000'], 'WCD50': ['T22X56X62', 'P14X75', 'P16X100', 'P24X50', 'P23X60', 'P10X70', 'P12X70', 'P8X65'], 'SNC': ['P25X500'], 'URETA': ['P20X500', 'P15X500', 'P60X500', 'P35X500', 'P50X500', 'P22X500', 'T3X200X300', 'P26X500', 'T1.5X200X300', 'T0.5X200X300', 'P10X500', 'T2X200X300', 'T1X200X300', 'T5X200X300', 'T15X200X300', 'P4X500', 'P6X500', 'P45X500'], 'NA30': ['T11X64X100', 'P36X100', 'T8X50X130', 'P7X50'], 'AION': ['T10X310X500'], 'CU': ['O5XO10X500', 'PBC-2C(120X60X4', 'PBC-2C(260X200X'], 'PPS': ['T10X200X200'], 'PRD9N': ['T12X60X100', 'T6X60X100', 'P13X70', 'P5X60'], 'EM10': ['T16.5X20.5X30.5'], 'C5210': ['T0.5X300X500', 'T0.3X300X500', 'T0.1X300X500'], 'AGW': ['P5X200', 'P6X200'], 'MCZ': ['P2.5X1000'], 'SSROD': ['P3.8X2000'], 'SK': ['TFG-0.03M1', 'TFG-0.08M1'], 'NAK80': ['P6*1000'], 'HPM75': ['P65X500'], 'XW10': ['T32X300X500']}
                context['dict_material_stages'] = dict_material_stages
                
                if request.FILES.get('pdfFile'):
                    pdf_file = request.FILES['pdfFile']

                    file_path = f'temp/{pdf_file.name}'

                    # Save the file using default_storage
                    with default_storage.open(file_path, 'wb') as destination:
                        for chunk in pdf_file.chunks():
                            destination.write(chunk)
                    file_path = 'media/' + file_path
    
                    pdf_path = static(file_path)
                    context['pdf_path'] = pdf_path  
                    return render(request, "thietlap_all.html", context)
                
                return render(request, "thietlap_all.html", context)


            return render(request, "thietlap_pdf.html", context)


    return render(request, "thietlap_detail.html")


from django.http import JsonResponse


def kiemtratuchu(request):

    all_request_info = RequestInfo.objects.all()
    return render(request, 'kiemtratuchu.html', {'all_request_info': all_request_info})

def tuchu_detail(request,request_number):

    # if request.method == 'POST':
    #     data = request.POST.get('savedValues')
    #     saved_values = json.loads(data)
    #     syc = saved_values[0][1]
    #     request_info = RequestInfo.objects.get(request_number = syc)

    #     list_cong_doan = saved_values[1][1:]
    #     list_employee = saved_values[2][1:]

    #     for index_kt in range(3, len(saved_values), 4):
    #         kt = saved_values[index_kt][0]

    #         list_max = saved_values[index_kt+1]
    #         list_min = saved_values[index_kt+2]
    #         list_okng = saved_values[index_kt+3]
    #         if index_kt == 3:
    #             StageTuchu.objects.filter(requirement=request_info).delete()
            
    #         inspections = []
    #         for index, (cd, ep,max, min, okng) in enumerate(zip(list_cong_doan,list_employee,list_max,list_min,list_okng)):
    #             max = None if max == '' else max
    #             min = None if min == '' else min
    #             okng = None if okng == '' else okng
                
    #             user = User.objects.get(username=ep)
    #             if index_kt == 3:
    #                 stage_tuchu = StageTuchu.objects.create(requirement = request_info, StageTuchu= cd, employee = user, stt= index+1)
    #                 Inspection.objects.filter(stage = stage_tuchu).delete()

    #             else:
    #                 stage_tuchu = StageTuchu.objects.get(requirement = request_info, StageTuchu= cd, employee = user, stt= index+1)

    #             inspections.append(Inspection(stage=stage_tuchu, inspect=kt, max_value=max, min_value=min, ok_ng=okng, stt=index + 1))

    #             # Inspection.objects.create(stage = stage_tuchu, inspect = kt, max_value = max, min_value = min,ok_ng = okng, stt= index+1)
    #         Inspection.objects.bulk_create(inspections)
    #     context = {'request_info': 'request_info'}


    #     return render(request, 'tuchu_detail.html', context)

    rep_number = 0 
    if "-" in request_number:
        request_and_rep = request_number.split('-')
        request_number = request_and_rep[0].strip()
        rep_number = request_and_rep[1].strip()

    request_info = get_object_or_404(RequestInfo, request_number=request_number,rep_number=rep_number)

    execution_times = ExecutionTime.objects.filter(employee_processing__request_info=request_info)

    employee_processing_instances = execution_times.values('employee_processing__id').distinct()

    employee_processing_list = []
    users_list = []

    for instance in employee_processing_instances:
        execution_times = ExecutionTime.objects.filter(employee_processing_id=instance['employee_processing__id'])
        execution_times = list(execution_times)
        if execution_times:
            for execution_time in execution_times:
                employee_processing = execution_time.employee_processing
                user = execution_time.user

        
                employee_processing_list.append(employee_processing)
                users_list.append(user)

    context = {'request_info': request_info, 'employee_processing_list': employee_processing_list,'users_list':users_list}
    stages_tuchu = StageTuchu.objects.filter(requirement=request_info)
    if stages_tuchu.exists():
        inspections = Inspection.objects.filter(stage__in=stages_tuchu)
        inspects = inspections.values_list('inspect', flat=True).distinct()
        # max_values = []
        # min_values = []
        # okngs = []
        inspects_dict = {}
        for inspect in inspects:
            max_values = inspections.filter(inspect=inspect).values_list('max_value', flat=True)
            min_values = inspections.filter(inspect=inspect).values_list('min_value', flat=True)
            okngs = inspections.filter(inspect=inspect).values_list('ok_ng', flat=True)
            length_lack = range(len(max_values),len(employee_processing_list))
            print(length_lack)

            inspects_dict[inspect] = {'max_values':max_values, 'min_values':min_values,'okngs':okngs,'length_lack':length_lack}


        
        context['stages_tuchu'] = stages_tuchu
        context['inspects_dict'] = inspects_dict

        # context['inspects'] = inspects
        # context['inspections'] = inspections
        # context['max_values'] = max_values
        # context['min_values'] = min_values
        # context['okngs'] = okngs

    return render(request, 'tuchu_detail2.html', context)


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import StageTuchu, Inspection
from django.contrib.auth.models import User

from django.db import transaction

@transaction.atomic
def save_kiemtratuchu(request):

    data = request.POST.get('savedValues')
    saved_values = json.loads(data)

    syc = saved_values[0][1]
    if "-" in syc:
        request_and_rep = syc.split('-')
        syc = request_and_rep[0].strip()
        rep_number = request_and_rep[1].strip()
    print(syc)

    request_info = RequestInfo.objects.get(request_number=syc)

    list_cong_doan = saved_values[1][1:]
    list_employee = saved_values[2][1:]

    if len(saved_values) > 3:
        for index_kt in range(3, len(saved_values), 4):
            kt = saved_values[index_kt][0]

            list_max = saved_values[index_kt + 1]
            list_min = saved_values[index_kt + 2]
            list_okng = saved_values[index_kt + 3]

            if index_kt == 3:
                StageTuchu.objects.filter(requirement=request_info).delete()

            inspections = []

            for index, (cd, ep, max_val, min_val, ok_ng) in enumerate(zip(list_cong_doan, list_employee, list_max, list_min, list_okng)):
                max_val = None if max_val == '' else max_val
                min_val = None if min_val == '' else min_val
                ok_ng = None if ok_ng == '' else ok_ng

                # user, _ = User.objects.get_or_create(username=ep)
                user = User.objects.get(username=ep)

                if index_kt == 3:
                    stage_tuchu = StageTuchu.objects.create(requirement=request_info, StageTuchu=cd, employee=user, stt=index + 1)
                    Inspection.objects.filter(stage=stage_tuchu).delete()
                else:

                    stage_tuchu,_ = StageTuchu.objects.get_or_create(requirement=request_info, StageTuchu=cd, employee=user, stt=index + 1)

                inspections.append(Inspection(stage=stage_tuchu, inspect=kt, max_value=max_val, min_value=min_val, ok_ng=ok_ng, stt=index + 1))

            Inspection.objects.bulk_create(inspections)

    else:
        StageTuchu.objects.filter(requirement=request_info).delete()

    response_data = {
        'success': True,
        'redirect_url': reverse('kiemtratuchu'),
    }


    return JsonResponse(response_data)


from django.db.models import F, Value
from django.db.models.functions import Concat
from django.db import models

def get_file_drawing(request):
    # all_orders = Order.objects.all()

    # for order in all_orders:
    #     order.drawing = f'order_drawings/{order.sno.sno}.pdf'
    #     order.save()


    all_orders = Order.objects.all()

    updated_orders = [
        Order(id=order.id, drawing=f'order_drawings/{order.sno.sno}.pdf')
        for order in all_orders
    ]

    Order.objects.bulk_update(updated_orders, ['drawing'])




# @require_POST
# def save_kiemtratuchu(request):
#     # try:

#     data = request.POST.get('savedValues')
#     saved_values = json.loads(data)
#     syc = saved_values[0][1]
#     request_info = RequestInfo.objects.get(request_number = syc)

#     list_cong_doan = saved_values[1][1:]
#     list_employee = saved_values[2][1:]

#     for index_kt in range(3, len(saved_values), 4):
#         kt = saved_values[index_kt][0]

#         list_max = saved_values[index_kt+1]
#         list_min = saved_values[index_kt+2]
#         list_okng = saved_values[index_kt+3]
#         if index_kt == 3:
#             StageTuchu.objects.filter(requirement=request_info).delete()
        
#         inspections = []
#         for index, (cd, ep,max, min, okng) in enumerate(zip(list_cong_doan,list_employee,list_max,list_min,list_okng)):
#             max = None if max == '' else max
#             min = None if min == '' else min
#             okng = None if okng == '' else okng
            
#             user = User.objects.get(username=ep)
#             if index_kt == 3:
#                 stage_tuchu = StageTuchu.objects.create(requirement = request_info, StageTuchu= cd, employee = user, stt= index+1)
#                 Inspection.objects.filter(stage = stage_tuchu).delete()

#             else:
#                 stage_tuchu = StageTuchu.objects.get(requirement = request_info, StageTuchu= cd, employee = user, stt= index+1)

#             inspections.append(Inspection(stage=stage_tuchu, inspect=kt, max_value=max, min_value=min, ok_ng=okng, stt=index + 1))

#             # Inspection.objects.create(stage = stage_tuchu, inspect = kt, max_value = max, min_value = min,ok_ng = okng, stt= index+1)
#         Inspection.objects.bulk_create(inspections)


#     response_data = {
#         'success': True,
#         'redirect_url': reverse('kiemtratuchu'),

#     }

#     return JsonResponse(response_data)

    # except Exception as e:
    #     return JsonResponse({'success': False, 'message': str(e)})






# @csrf_exempt
# def save_request_info(request):


# def thietlap_detail(request):
#     materials = None
#     specification = None
#     processing_times = None

#     if request.method == 'POST':
#         s_no = request.POST.get('selected_order_sno')
#         so_yeu_cau = request.POST.get('so_yeu_cau')
#         so_luong = request.POST.get('so_luong')
#         loai_s_chuan = request.POST.get('loai_s_chuan')


#         if loai_s_chuan == 'Có S chuẩn':
#             # Assuming that s_no is related to the Sno model
#             sno_object = get_object_or_404(Sno, sno=s_no)

#             # Fetch the first Order object based on sno and type_s
#             order_object = Order.objects.filter(sno=sno_object, type_s=loai_s_chuan).first()

#             if order_object:
#                 # Get materials and specification from the Order object
#                 materials = order_object.materials
#                 specification = order_object.specification

#                 # Fetch all related ProcessingTime objects
#                 processing_times = ProcessingTime.objects.filter(sno=sno_object)

#                 context = {'s_no': s_no, 'so_yeu_cau': so_yeu_cau, 'so_luong': so_luong, 'loai_s_chuan': loai_s_chuan,
#                         'materials': materials, 'specification': specification, 'processing_times': processing_times}

#                 return render(request, "thietlap_detail.html", context)

#             # # try:
#             # # Assuming that s_no is related to the Sno model
#             # sno_object = get_object_or_404(Sno, sno=s_no)

#             # # Fetch the Order object based on sno and type_s
#             # order_object = get_object_or_404(Order, sno=sno_object, type_s=loai_s_chuan)

#             # # Get materials and specification from the Order object
#             # materials = order_object.materials
#             # specification = order_object.specification

#             # # Fetch all related ProcessingTime objects
#             # processing_times = ProcessingTime.objects.filter(sno=sno_object)

#             # context = {'s_no': s_no, 'so_yeu_cau': so_yeu_cau, 'so_luong': so_luong, 'loai_s_chuan': loai_s_chuan,
#             #         'materials': materials, 'specification': specification, 'processing_times': processing_times}

#             # return render(request, "thietlap_detail.html", context)
#             # # except:
#             # #     pass

#     return render(request, "thietlap_detail.html")


# def nhanvien(request):
#     materials = Material.objects.all()
#     processingStages = ProcessingStage.objects.all()

#     pdf_path = ''
#     context = {'materials': materials}

#     context['loop_times'] = range(1, 100)
#     context['processingStages'] = processingStages

#     if request.method == 'POST' and request.FILES.get('pdfFile'):
#         pdf_file = request.FILES['pdfFile']
#         file_path = f'temp/{pdf_file.name}'

#         # Save the file using default_storage
#         with default_storage.open(file_path, 'wb') as destination:
#             for chunk in pdf_file.chunks():
#                 destination.write(chunk)
#         file_path = 'media/' + file_path
#         pdf_path = static(file_path)
#     context['pdf_path'] = pdf_path
#     # return render(request, 'your_template.html', {'form': form})
#     return render(request, "nhanvien.html", context)




def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
     
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with the name of your home URL pattern
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        # else:
        #     messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'form': form})

from .models import NameEmployee
def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data['full_name']
            NameEmployee.objects.create(user=user, name=full_name)
            login(request, user)

            return redirect('home') 
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')

    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def user_logout(request):
    logout(request)
    
    return redirect('user_login')

