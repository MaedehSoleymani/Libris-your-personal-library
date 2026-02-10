def reset_password_email(reset_link):
    return f"""
    <div style="direction: rtl; font-family: 'Open Sans', sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #0066ff; margin-bottom: 20px;">کاربر گرامی،</h2>
        
        <p style="margin-bottom: 15px;">
            درخواستی برای بازیابی رمز عبور حساب کاربری شما در لیبریس دریافت کرده‌ایم.
        </p>
        
        <p style="margin-bottom: 15px;">
            برای تعیین رمز عبور جدید، لطفاً روی دکمه زیر کلیک کنید:
        </p>
        
        <div style="text-align: center; margin: 25px 0;">
            <a href="{reset_link}" 
               style="background: #0066ff; color: white; padding: 12px 30px; 
                      text-decoration: none; border-radius: 6px; display: inline-block;
                      font-weight: 600; font-size: 16px;">
                تغییر رمز عبور
            </a>
        </div>
        
        <div style="background: #fff8e1; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
            <strong>⏳ توجه:</strong><br>
            این لینک فقط به مدت ۳۰ دقیقه معتبر است و پس از آن منقضی می‌شود.
        </div>
        
        <p style="margin-bottom: 15px;">
            اگر شما این درخواست را ارسال نکرده‌اید، می‌توانید با خیال راحت این ایمیل را نادیده بگیرید.
        </p>
        
        <p style="margin-top: 25px; color: #666; font-style: italic;">
            با آرزوی مطالعه‌ای لذت‌بخش 📚<br>
            <strong>تیم Libris</strong>
        </p>
    </div>
    """