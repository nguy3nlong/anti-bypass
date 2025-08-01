# anti-bypass  
mang về làm của riêng thì chỉ cần 1 dòng credit thôi  
Anti Bypass link rút gọn  
**Main URL: `anti-bypass-shortlinks.vercel.app`**  
1. **Kiểm tra tình trạng link Yeumoney**  
```
POST /yeumoney/check
```
Body:  
`cookies` (string): Cookies tài khoản Yeumoney  
  
`id` (string): ID Link Yeumoney  
VD: Nếu link là yeumoney.com/abc123 thì id sẽ là abc123  
  
`t` (string): Thời gian  
VD: 'True', 'False' nếu là 'True' sẽ tự động chờ 15s để hệ thống Yeumoney cập nhật trước khi kiểm tra tình trạng link  

*curl Example*:
```
curl -X POST https://anti-bypass-shortlinks.vercel.app/yeumoney/check \
  -H "Content-Type: application/json" \
  -d '{
    "id": "abc123",
    "cookies": "user=abc123; token=abc123; user_token=abc123",
    "t": "True"
  }'
```  
*Response Example*:  
Lỗi:  
- ID Yeumoney chưa chính xác hoặc cookies sai: `{'e': 'Vui lòng cung cấp id Yeumoney'}`  
- Chưa có json trong request gửi đi: `{'e': 'Vui lòng thêm json vào request'}`  
- Cookies tài khoản sai: `{'e': 'Vui lòng thêm cookies tài khoản hợp lệ'}`
- Chưa cung cấp t (thời gian) trong body: `{'e': 'Vui lòng cung cấp lựa chọn time'}`
- ID sai hoặc server bị lỗi: `{'f': 'id bạn cung cấp không hợp lệ hoặc Server lỗi'}`
  
Thành công:  
- Người dùng đã vượt link và không bypass: `{'s': 'Xác thực thành công'}`  
- Người dùng vượt link nhưng đã bypass: `{'f': 'Người dùng chưa vượt link'}`  

2. **Kiểm tra tình trạng link BBMKTS**  
```
POST /bbmkts/check
```
Body:  
`cookies` (string): Cookies tài khoản BBMKTS  
  
`id` (string): ID Link BBMKTS  
  
`t` (string): Thời gian  
VD: 'True', 'False' nếu là 'True' sẽ tự động chờ 15s để hệ thống BBMKTS cập nhật trước khi kiểm tra tình trạng link  

*curl Example*:
```
curl -X POST https://anti-bypass-shortlinks.vercel.app/bbmkts/check \
  -H "Content-Type: application/json" \
  -d '{
    "id": "abc123",
    "cookies": "",
    "t": "True"
  }'
```  
*Response Example*:  
Lỗi:  
- ID BBMKTS chưa chính xác hoặc cookies sai: `{'e': 'Vui lòng cung cấp id Link BBMKTS'}`  
- Chưa có json trong request gửi đi: `{'e': 'Vui lòng thêm json vào request'}`  
- Cookies tài khoản sai: `{'e': 'Vui lòng thêm cookies tài khoản hợp lệ'}`
- Chưa cung cấp t (thời gian) trong body: `{'e': 'Vui lòng cung cấp lựa chọn time'}`
- ID sai hoặc server bị lỗi: `{'f': 'id bạn cung cấp không hợp lệ hoặc Server lỗi'}`
- JSON của link trả về không hợp lệ hoặc ID sai: `{'f': 'Lỗi server, json không hợp lệ'}`
- Không có dữ liệu của ID mà bạn đã cung cấp: `{'f': 'Không có dữ liệu trong link, vui lòng kiểm tra lại ID'}`  
  
Thành công:  
- Người dùng đã vượt link và không bypass: `{'s': 'Xác thực thành công'}`  
- Người dùng vượt link nhưng đã bypass: `{'f': 'Người dùng chưa vượt link'}`  
  
Het roi
