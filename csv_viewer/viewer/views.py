from django.shortcuts import render
import pandas as pd
from .forms import UploadFileForm

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
            df = df.iloc[:50]
            df_html = df.to_html(classes='table table-bordered table-hover table-sm table-striped',
                                index=False,
                                border=0,
                                justify='center',
                                escape=False)
        except Exception as e:
            df_html = f"<p style='color:red;'>Error reading file: {e}</p>"
    return render(request, 'viewer/upload.html', {'form': form, 'df_html': df_html, 'row_count': row_count, 'column_types': column_types})