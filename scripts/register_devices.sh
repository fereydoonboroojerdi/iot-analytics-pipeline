aws iot register-thing --template-body file://device_template.json \
  --parameters '{"SerialNumber":"SN-123","Factory":"Plant-17"}'