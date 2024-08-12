from django.contrib import admin
from .models import Document, DocumentSubmission

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0  # Do not show extra blank forms

class DocumentSubmissionInline(admin.TabularInline):
    model = DocumentSubmission
    extra = 0

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'document_type', 'file_name', 'uploaded_at', 'parsing_status')
    search_fields = ('customer__user__username', 'file_name')
    list_filter = ('document_type', 'parsing_status')

@admin.register(DocumentSubmission)
class DocumentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'document', 'submitted_at', 'status')
    search_fields = ('customer__user__username', 'document__file_name')
    list_filter = ('status',)