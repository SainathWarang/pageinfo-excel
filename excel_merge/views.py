import re
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
import io

def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        error_files = []

        # Create an empty DataFrame to store the merged data
        merged_df = pd.DataFrame()

        # Iterate over each uploaded file
        for file in files:
            try:
                # Read the uploaded file using pandas
                df = pd.read_excel(file)

                # Check if the required columns (A, B, C) are present
                if 'A' not in df.columns or 'B' not in df.columns or 'C' not in df.columns:
                    error_files.append(file.name)
                    continue

                # Extract mobile numbers from the C column
                df['C'] = df['C'].apply(extract_mobile_number)

                # Remove rows where C column is empty or mobile number extraction failed
                df = df.dropna(subset=['C'])

                # Select the specified columns
                selected_columns = ['A', 'B', 'C']
                df_selected = df[selected_columns]

                # Append the selected columns to the merged DataFrame
                merged_df = pd.concat([merged_df, df_selected])
            except Exception as e:
                error_files.append(file.name)

        # Remove rows where C column is empty
        merged_df = merged_df.drop_duplicates(subset=['C'])

        # Generate a new Excel file
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            merged_df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)

        # Set the appropriate response headers
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        my_text_value = request.POST.get('my_text_field')
        print(my_text_value)
        combined_file_name = my_text_value + ".xlsx"
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(combined_file_name)

        # Check if there were any files with missing or incorrect columns
    # ...
        if error_files:
          error_message = "The following files have not column name A B C, please, can you correct them : {}".format(", ".join(error_files))
          response['X-Error-Message'] = error_message
          return render(request, 'upload.html', {'error_message': error_message})
        return response
    return render(request, 'upload.html')


def extract_mobile_number(value):
    # Regex pattern to match 10-digit numbers
    pattern = r"\d{5} \d{5}"

    # Extract the mobile number from the value using regex
    mobile_number = re.search(pattern, str(value))

    if mobile_number:
        return mobile_number.group().replace(" ", "")  # Remove the space in the mobile number
    return ''

#     if request.method == 'POST':
#         files = request.FILES.getlist('files')

#         # Create an empty DataFrame to store the merged data
#         merged_df = pd.DataFrame()

#         # Iterate over each uploaded file
#         for file in files:
#             # Read the uploaded file using pandas
#             df = pd.read_excel(file)

#             # Extract mobile numbers from the C column
#             df['C'] = df['C'].apply(extract_mobile_number)

#             # Remove rows where C column is empty or mobile number extraction failed
#             df = df.dropna(subset=['C'])

#             # Select the specified columns
#             selected_columns = ['A', 'B', 'C']
#             df_selected = df[selected_columns]

#             # Append the selected columns to the merged DataFrame
#             merged_df = pd.concat([merged_df, df_selected])

#         # Remove rows where C column is empty
#         merged_df = merged_df.drop_duplicates(subset=['C'])

#         # Generate a new Excel file
#         output = io.BytesIO()
#         with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#             merged_df.to_excel(writer, index=False, sheet_name='Sheet1')
#         output.seek(0)

#         # Set the appropriate response headers
#         response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         my_text_value = request.POST.get('my_text_field')
#         print(my_text_value)
#         combined_file_name = my_text_value + ".xlsx"
#         response['Content-Disposition'] = 'attachment; filename="{}"'.format(combined_file_name)
#         return response

#     return render(request, 'upload.html')


# def extract_mobile_number(value):
#     # Regex pattern to match 10-digit numbers
#     pattern = r"\d{5} \d{5}"

#     # Extract the mobile number from the value using regex
#     mobile_number = re.search(pattern, str(value))

#     if mobile_number:
#         return mobile_number.group().replace(" ", "")  # Remove the space in the mobile number
#     return ''

    # if request.method == 'POST':
    #     files = request.FILES.getlist('files')

    #     # Create an empty DataFrame to store the merged data
    #     merged_df = pd.DataFrame()

    #     # Iterate over each uploaded file
    #     for file in files:
    #         # Read the uploaded file using pandas
    #         df = pd.read_excel(file)

    #         # Remove rows where C column is empty
    #         df = df.dropna(subset=['C'])

    #         # Select the specified columns
    #         selected_columns = ['A', 'B', 'C']
    #         df_selected = df[selected_columns]

    #         # Append the selected columns to the merged DataFrame
    #         merged_df = pd.concat([merged_df, df_selected])

    #     # Generate a new Excel file
    #     output = io.BytesIO()
    #     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    #         merged_df.to_excel(writer, index=False, sheet_name='Sheet1')
    #     output.seek(0)

    #     # Set the appropriate response headers
    #     response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #     my_text_value = request.POST.get('my_text_field')
    #     print(my_text_value)
    #     combined_file_name = my_text_value+".xlsx"
    #     response['Content-Disposition'] = 'attachment; filename="{}"'.format(combined_file_name)
    #     return response

    # return render(request, 'upload.html')
