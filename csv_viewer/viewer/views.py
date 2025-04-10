from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import pandas as pd
from .forms import UploadFileForm

import json

def upload_file(request):
    form = UploadFileForm()
    
    df_html = None
    row_count = None
    column_names = None
    column_types = None

    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            csv_file = request.FILES['file']
            df = pd.read_csv(csv_file)
            row_count = len(df)
            column_types = dict(df.dtypes)
            df_html = df.to_html(classes='table table-bordered table-hover table-sm table-striped',
                                index=False,
                                border=0,
                                justify='center',
                                escape=False)
        except Exception as e:
            df_html = f"<p style='color:red;'>Error reading file: {e}</p>"
    return render(request, 'viewer/upload.html', {'form': form, 'df_html': df_html, 'row_count': row_count, 'column_types': column_types})

@require_http_methods(["POST"])
def update_row(request):
    row_index = 1
    try:
        row_index = int(request.POST.get("rowIndex"))
        row_data = json.loads(request.POST.get("rowData"))
        
        df_json = request.session.get("df_data")
        if not df_json:
            return JsonResponse({"success": False, "error": "No data found in session"})
        
        df = pd.read_json(df_json, orient='split')
        df.iloc[row_index] = row_data
        request.session["df_data"] = df.to_json(orient='split')
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})