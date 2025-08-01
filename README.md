# anti-bypass

Anti Bypass link rút gọn  
**Main URL: anti-bypass-shortlinks.vercel.app**  
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
