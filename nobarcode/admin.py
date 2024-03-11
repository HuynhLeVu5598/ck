# admin.py
from django.contrib import admin
from .models import Material, ProcessingStage, ProcessingTime, Order, Sno, RequestSttProcessing,ExecutionTime
from import_export import resources
from import_export.admin import ImportExportModelAdmin

admin.site.register(RequestSttProcessing)
admin.site.register(ExecutionTime)



class SnoAdmin(admin.ModelAdmin):
    search_fields = ['sno']  

admin.site.register(Sno, SnoAdmin)

class ProcessingStageResource(resources.ModelResource):
    class Meta:
        model = ProcessingStage
        fields = ('process_name',)
        import_id_fields = ('process_name',)  



class ProcessingStageAdmin(ImportExportModelAdmin):
    resource_class = ProcessingStageResource
    list_display = ('process_name',)
    search_fields = ['process_name'] 

admin.site.register(ProcessingStage, ProcessingStageAdmin)


class MaterialResource(resources.ModelResource):
    class Meta:
        model = Material
        fields = ('name',)
        import_id_fields = ('name',)  

class MaterialAdmin(ImportExportModelAdmin):
    resource_class = MaterialResource
    list_display = ('name',)
    search_fields = ['name'] 

admin.site.register(Material, MaterialAdmin)

from .models import StageTuchu, Inspection, WorkDate, NameEmployee
admin.site.register(StageTuchu)
admin.site.register(Inspection)
admin.site.register(WorkDate)
admin.site.register(NameEmployee)




class ProcessingTimeResource(resources.ModelResource):
    class Meta:
        model = ProcessingTime
        fields = ('sno', 'stt', 'stage__process_name', 'time_required',)
        import_id_fields = ('sno', 'stt','stage__process_name','time_required')

class ProcessingTimeAdmin(ImportExportModelAdmin):
    resource_class = ProcessingTimeResource
    list_display = ('sno', 'stt','stage', 'time_required',)

admin.site.register(ProcessingTime, ProcessingTimeAdmin)



from .models import EmployeeProcessing

admin.site.register(EmployeeProcessing)


from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Order

class OrderResource(resources.ModelResource):
    class Meta:
        model = Order

class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    list_display = ('sno', 'type_s','materials','specification')



admin.site.register(Order, OrderAdmin)









from .models import RequestInfo

class RequestInfoResource(resources.ModelResource):
    class Meta:
        model = RequestInfo
        fields = ('request_number', 'quantity',)
        import_id_fields = ('request_number',)

class RequestInfoAdmin(ImportExportModelAdmin):
    resource_class = RequestInfoResource
    list_display = ('request_number', 'quantity', )
    search_fields = ['request_number']  


admin.site.register(RequestInfo, RequestInfoAdmin)


# class DrawingResource(resources.ModelResource):
#     class Meta:
#         model = Drawing
#         fields = ('order__sno', 'pdf',)
#         import_id_fields = ('order__sno',)

# class DrawingAdmin(ImportExportModelAdmin):
#     resource_class = DrawingResource
#     list_display = ('order_sno', 'pdf',)

#     def order_sno(self, obj):
#         return obj.order.sno

#     order_sno.short_description = 'Số đơn hàng'

# admin.site.register(Drawing, DrawingAdmin)


