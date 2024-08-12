from django.contrib import admin
from .models import CustomerAccount
from apps.fileintake.admin import DocumentInline, DocumentSubmissionInline  # Import the inlines

@admin.register(CustomerAccount)
class CustomerAccountAdmin(admin.ModelAdmin):
    list_display = ('user_f_name', 'user_l_name', 'user_email', 'user_phone', 'created_at')
    search_fields = ('user_l_name', 'user_email', 'user_phone')
    inlines = [DocumentInline, DocumentSubmissionInline]  # Add the inlines


# class DocumentSubmissionInline(admin.TabularInline):
#     model = DocumentSubmission
#     extra = 0
#     readonly_fields = ('submitted_at', 'status')
#     can_delete = False
#     max_num = 0
#
# @admin.register(Document)
# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ('customer', 'document_type', 'file_name', 'uploaded_at', 'upload_status')
#     list_filter = ('document_type', 'upload_status', 'uploaded_at')
#     search_fields = ('customer__user__username', 'file_name')
#     readonly_fields = ('uploaded_at', 'upload_status')
#     inlines = [DocumentSubmissionInline]
#
# @admin.register(DocumentSubmission)
# class DocumentSubmissionAdmin(admin.ModelAdmin):
#     list_display = ('customer', 'document', 'submitted_at', 'status')
#     list_filter = ('status', 'submitted_at')
#     search_fields = ('customer__user__username', 'document__file_name')
#     readonly_fields = ('submitted_at',)