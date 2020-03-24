from config import settings
from libraries.Functions import base64encode


def welcome_email(request):
    content = """\
    <body style="margin: 0;padding: 0;">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" >
        <table width="595" border="0" cellspacing="0" cellpadding="0" align="left">
            <tr>
                <td><a href="#" target="_blank"><img src="<?php echo base_url(); ?>dist/website/images/mailer/header_top.jpg" alt=""></a> </td>
            </tr>
            <tr>
                <td>
                    <table width="100%" border="0" cellspacing="0" cellpadding="0">
                        <table>
                            <tr>
                                <td style="font-size:16px;color: #181b14;line-height: 24px;font-family: arial;">
                                    Dear student,
                                    <br>
                                    <br><i>Congratulations!!</i>
                                    <br>
                                    <br>You have <b>Earned $25</b> in your Mentyor wallet.
                                    <br><b>Earn $50</b> more by referring a friend. 
                                    <br>
                                    <br>The offer is not over!!
                                    <br>
                                    <br><b>Earn 10%  cashback</b> on each successful completion of your assignment.
                                    <br>
                                    <br><small> Also follow us on 
                                    <a href="https://www.facebook.com/Mentyor/">Facebook</a>,
                                    <a href="https://twitter.com/MentyorS">Twitter</a>, 
                                    <a href="https://www.linkedin.com/company/mentyor/">LinkedIn </a> & 
                                    <a href="https://www.instagram.com/mentyor_gd/">Instagram</a> for more offers!!<small>
                                    <div style="border-left:3px solid #acacac;padding-left:5px">
                                    </div>
                                    Regards,<br>
                                    Support Team<br>
                                    <a href="https://www.mentyor.com/">www.mentyor.com</a>
                                </td>
                            </tr>
                        </table>
                    </table>
                </td>
            </tr>
            <tr>
                <td><a href="#" target="_blank"><img src="<?php echo base_url(); ?>dist/website/images/mailer/header_bottom.jpg" alt=""></a> </td>
            </tr>
        </table>
    </table>
</body>
    """
    return content


def forgot_pwd_email_content(user, token, path=None):
    url_encoded_data = base64encode(user)
    url = path + "/reset-password/?token=" + token
    content = """\
    <body style="margin: 0;padding: 0;">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" >
        <table width="595" border="0" cellspacing="0" cellpadding="0" align="left">
            <tr>
                <td width="10%">&nbsp;</td>
                <td style="font-size:16px;color: #181b14;line-height: 24px;font-family: arial;">
                    <br><br> Hi User <br><br>
                    <span style="line-height:34px;">
                        Email :   <strong>""" + user.email + """</strong>
                        <br>
                        <strong>
                            <a href=""" + url + """>Click here</a>
                        </strong> to reset your password.
                    </span>
                </td><td width="5%">&nbsp;</td>
            </tr>
        </table>
    </table>
</body>
    """
    return content

def reset_pwd_email_content(user, path=None):

    url_encoded_data = base64encode(user)
    url = "https://www.analyticssteps.com/login"

    content = """\
    <body style="margin: 0;padding: 0;">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" >
        <table width="595" border="0" cellspacing="0" cellpadding="0" align="left">
            <tr>
                <td width="10%">&nbsp;</td>
                <td style="font-size:16px;color: #181b14;line-height: 24px;font-family: arial;">
                    <br><br> Hi """+ user.name +""" <br><br>
                    <span style="line-height:34px;">
                        <strong>Your password has been reset successfully!</strong>
                        <br>
                        <strong>
                            <a href=""" + url + """>Click here</a>
                        </strong> to return to the login page.
                    </span>
                </td><td width="5%">&nbsp;</td>
            </tr>
        </table>
    </table>
</body>
    """
    return content


def adminusr_resetpwd_emailcontent(user, token, path=None):
    """
    Email content fot reset password for admin users
    :param user:
    :param token:
    :param path:
    :return:
    """
    url_encoded_data = base64encode(user)
    url = "http://192.168.1.19:4200/pages/resetpassword?token=" + token
    content = """\
    <body style="margin: 0;padding: 0;">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" >
        <table width="595" border="0" cellspacing="0" cellpadding="0" align="left">
            <tr>
                <td width="10%">&nbsp;</td>
                <td style="font-size:16px;color: #181b14;line-height: 24px;font-family: arial;">
                    <br><br> Hi User <br><br>
                    <span style="line-height:34px;">
                        Email :   <strong>""" + user.email + """</strong>                                                           
                        <br> 
                        <strong>
                            <a href=""" + url + """>Click here</a>
                        </strong> to reset your password.   
                    </span>		
                </td><td width="5%">&nbsp;</td>
            </tr>
        </table>
    </table>
</body>
    """
    return content


def new_adminusr_resetpwd_email(user, token, path=None):
    """
    Email content fot reset password for first time admin users
    :param user:
    :param token:
    :param path:
    :return:
    """
    url_encoded_data = base64encode(user)
    url = "http://192.168.1.19:4200/pages/resetpassword/?token=" + token
    content = """\
    <body style="margin: 0;padding: 0;">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" >
        <table width="595" border="0" cellspacing="0" cellpadding="0" align="left">
            <tr>
                <td width="10%">&nbsp;</td>
                <td style="font-size:16px;color: #181b14;line-height: 24px;font-family: arial;">
                    <br>Hi """ + user.name + """ <br><br>
                    Your account has been created as """ + user.group_name + """ in Mentyor.com.<br>
                    <span style="line-height:34px;">
                        Email :   <strong>""" + user.email + """</strong>                                                           
                        <br> 
                        <strong>
                            <a href=""" + url + """>Click here</a>
                        </strong> to reset your password.   
                    </span>		
                </td><td width="5%">&nbsp;</td>
            </tr>
        </table>
    </table>
</body>
    """
    return content


def refer_friend_email(referred_to, referred_by, refer_id):
    """
    Email content fot reset password for first time admin users
    :param user:
    :param token:
    :param path:
    :return:
    """
    # url_encoded_data = base64encode(user)
    url = "http://192.168.1.19:8000/register/?refer_code=" + refer_id
    content = """\
    <body style="margin: 0;padding: 0;">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" >
        <table width="595" border="0" cellspacing="0" cellpadding="0" align="left">
            <tr>
                <td width="10%">&nbsp;</td>
                <td style="font-size:16px;color: #181b14;line-height: 24px;font-family: arial;">
                <br> Hi """ + referred_to['name'] + """ <br>
                    Your Friend <b>""" + referred_by.name + """</b> with email id """ + referred_by.email + """ referred you for the Mentyor. 
                    Signup with  this link <a href='""" + url + """'> Click here to register</a> on Mentyor and dive in new learning experience.
                
                <br>
                We look forward to some positive and innovative actions in Mentyor. </td><td width="5%">&nbsp;</td>
            </tr>
        </table>
    </table>
</body>
    """
    return content


def career_page_email(name):
    content = """\
            <!doctype html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>AnalyticsStep | Career</title>
        </head>
        
        <body style="margin: 0;padding: 0;">
        <table width="100%" border="0" cellspacing="0" cellpadding="0">
         
            <tr>
              <td><table width="600" border="0" cellspacing="0" cellpadding="0" align="center" style="border: 1px solid #eee">
          
            <tr><td align="center"> <table width="90%" border="0" cellspacing="0" cellpadding="0" align="center">
           
        <tr><td style="line-height:15px;font-size: 0;" height="15">&nbsp;</td></tr>
            <tr><td align="right"><a href="#"><img src="http://www.codeflowtech.com/demo/mentyor-new/mailer/images/my-account.jpg" alt="" ></a></td></tr>	  
        
                <tr><td align="center"><a href="#"><img src="http://www.codeflowtech.com/demo/mentyor-new/mailer/images/mentyor-logo.jpg" alt="" ></a></td></tr>	  
                <tr><td style="line-height:35px;font-size: 0;" height="35">&nbsp;</td></tr>
                <tr><td style="font-family:Arial;font-size: 14px;color: #111111;font-weight: 600">Dear """ + name + """,</td></tr>
                 <tr><td style="line-height:30px;font-size: 0;" height="30">&nbsp;</td></tr>
                <tr><td style="font-family:Arial;font-size: 14px;color: #111111;font-weight: 400;">Thank you for exploring the career oppurtunities with <a href="https://www.analyticssteps.com" style="color:#111111;text-decoration: none;" target="_blank">AnalyticsSteps</a></td></tr>
                <tr><td style="line-height:10px;font-size: 0;" height="10">&nbsp;</td></tr>
                <tr><td style="font-family:Arial;font-size: 14px;color: #111111;font-weight: 400;line-height: 18px;">Your request has been successfully submitted, our recuiretment team will contact you soon.</td></tr>
                <tr><td style="line-height:10px;font-size: 0;" height="10">&nbsp;</td></tr>
               
                
                        </table> </td></tr>
                        
                        
                            <tr><td style="line-height:40px;font-size: 0;" height="40">&nbsp;</td></tr>

                    <!-- start six box-- -->
                          <tr><td style="line-height:35px;font-size: 0;" height="35">&nbsp;</td></tr>
                        <tr><td align="center"><table width="90%" border="0" cellspacing="0" cellpadding="0">
                        <tr><td style="font-family:Arial;font-size: 14px;color: #111111;font-weight:400;line-height: 18px;">All The Best<br>
                                    Thanks & Regards<br>
                                    Team Analytics Steps </td></tr>
                    </table>
                    </td></tr>
                </table>
                </td>
                    </tr>
                  
</table>

</body>
</html>
"""
    return content


def career_request_email(email, resume, role, first_name, last_name):

    resume = "https://analyticssteps.com" + resume
    content = """\
                <!doctype html>
            <html>
            <head>
            <meta charset="utf-8">
            <title>Analytics Steps | Career</title>
            </head>
            <body style="margin: 0;padding: 0;">
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr><td style="font-family:Arial;font-size: 14px;color: #111111;font-weight: 600">Dear """ + 'admin' + """,</td></tr>
                    <tr><td style="font-family:Arial;font-size: 14px;color: #111111;font-weight: 400;">New career request! </td></tr>
                    <tr><td style="font-family:Arial;font-size: 14px;color: #111111;font-weight: 400;line-height: 18px;">   Name - """ + first_name + " " + last_name + """</td></tr>
                    <tr><td style="font-family:Arial;font-size: 14px;color: #111111;font-weight: 400;line-height: 18px;">Email- """ + email + """</td></tr>
                    <tr><td style="font-family:Arial;font-size: 14px;color: #111111;font-weight: 400;line-height: 18px;">Role - """ + role + """</td></tr>
                    <tr><td style="font-family:Arial;font-size: 14px;color: #111111;font-weight: 400;line-height: 18px;">Resume - <a href=""" + resume + """>View Resume</a></td></tr>
                    <tr><td style="line-height:10px;font-size: 0;" height="10">&nbsp;</td></tr>
    </table>
    </body>
    </html>
    """
    return content


def career_templates(position):
    content = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                                <html xmlns="http://www.w3.org/1999/xhtml">
                                <head>
                                <title>Analytics Steps  |  Emailer</title>
                                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                                <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0"/>
                                </head>
                                <body>
                                 <table width="100%" border="0">
                                 <tbody>
                                <td><p  style="font-size: 16px;font-weight:500;line-height: 22px; color: #000000;font-family: Arial;">Dear Candidate, <br><br>
                                
                                Thank you for applying to the position of {} with us. Your candidature  is underprocess. Our recruiting team will review your profile and revert back to you if we find you suitable with job’s requirements.
                                <br><br>
                                    Thank you<br>
                                    Team <a href= "https://www.analyticssteps.com/">Analytics Steps</a></p></td>
                                </tbody>
                                </table>
                                </body>
                                </html>
                                    """.format(position)
    return content


def news_subscribe():
    content="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                <title>Analytics Steps  |  Emailer</title>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0"/>
                </head>
                  <table>
                <body>
                <td><p  style="font-size: 16px;font-weight:500;line-height: 22px; color: #000000;font-family: Arial;">Dear Subscriber, <br><br>
                
                We’d appreciate your endeavor for subscription and assure you of providing the latest services. Stay in tune with latest <a href="https://www.analyticssteps.com/blogs"> blogs</a> and <a href="https://www.analyticssteps.com/news">news</a>.
                <br><br>
                Thank you<br>
                Team <a href= "https://www.analyticssteps.com/">Analytics Steps</a></p>

                </table>
                </body>
                </html>"""

    return content


def reg_email(user):
    content="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Analytics Steps  |  Emailer</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0"/>
</head>
<body>
<table width="100%" border="0">
<td><p  style="font-size: 16px;font-weight:500;line-height: 22px; color: #000000;font-family: Arial;">Dear """+ user.name.title() +""" <br><br>

We are overwhelmed with your registration, it is a gentle note for your registration confirmation. Herewith, you can <a href="https://www.analyticssteps.com/login" target="_blank" style="color:#126bff;text-decoration: none;">login here. </a>
<br><br>
Thank you</p>
</td>
</table>
</body>
</html>"""
    return content


def blog_request():
    content="""
                            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                        <html xmlns="http://www.w3.org/1999/xhtml">
                        <head>
                        <title>Analytics Steps  |  Emailer</title>
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0"/>
                        </head>
                        
                        <body>
                            <table width="100%" border="0">
                          <tbody>
                            <tr>
                              <td align="center"><table width="600"   border="0" align="center" cellpadding="0" cellspacing="0" style="border: 1px solid #eeeeee;">
                          <tbody>
                              <tr><td height="22" align="left"> </td></tr>
                                <tr><td align="center">
                                    <table   width="100%"  border="0" cellpadding="0" cellspacing="0">


                        <tr>

                        <td width="20" align="left"> </td>
                        <td align="left"><a href="https://www.analyticssteps.com" target="_blank"><img src="https://analyticssteps.com/backend/media/mailer-images/logo.jpg"  alt="" width="282" ></a></td>

                        <td align="right" valign="middle" height="25"><img src="https://analyticssteps.com/backend/media/mailer-images/icn_email.jpg" height="15" alt="" ></td>
                        <td align="right" width="164" valign="middle" height="25"><a href="mailto:info@analyticssteps.com" target="_blank" style="line-height: 25px;font-family: Arial;font-size: 14px;font-weight:500; color: #000000;text-decoration: none;padding-left: 5px;"> info@analyticssteps.com</a></td>
                        <td align="right" width="20"></td>

                        </tr>


                         
                        </table>
                                </td></tr>
                              <tr><td height="16" align="left"> </td></tr>

                                <tr><td><img src="https://analyticssteps.com/backend/media/mailer-images/ban_thank_1.jpg" width="600" alt="" align="left"> </td></tr>
                                <tr><td><img src="https://analyticssteps.com/backend/media/mailer-images/ban_thank_2.jpg" width="600" alt="" align="left"> </td></tr>

                                <tr><td align="center">
                                    <table   width="100%"  border="0" cellpadding="0" cellspacing="0">


                        <tr>

                        <td width="20"> </td>
                        <td><p  style="font-size: 16px;font-weight:500;line-height: 22px; color: #000000;font-family: Arial;">Dear candidate, <br><br>
                        
                        We are delighted to receive a blog response from your end, your time and efforts mean a lot for us.
                        <br><br>
                        Our technical team will examine your blog and communicate to you shortly for further process. In the meantime, you are requested to have a look at other blogs by visiting the company’s website <a href="https://www.analyticssteps.com/" target="_blank" style="color:#126bff;text-decoration: none;">www.analyticssteps.com</a>.
                        
                        
                        <br><br>
                        Thank you</p></td>
                            
                        
                        <td align="right" width="20"></td>
                            
                        </tr>
                         
                            
                         
                        </table>
                                </td></tr>
                        <tr><td height="25"> </td></tr>
                              
                        <!--<!-- -------------		fotter start 	------------- -->	  
                        <tr><td bgcolor="#314f74" style="padding: 12px 0" align="center">
                            
                        
                                <table width="100%"  border="0" cellpadding="0" cellspacing="0" align="center"> 
                         
                        <tr>
                        
                        <td width="20" align="left"> </td>
                         <td width="120" align="left" valign="middle" height="25" style="font-family: Arial;font-size: 14px;font-weight:500;line-height: 25px; color: #ffffff;text-decoration: none;">Stay Connected</td>
                        <td align="left" width="25" valign="middle"><a href="https://www.facebook.com/AnalyticsStep" target="_blank"><img src="https://analyticssteps.com/backend/media/mailer-images/icn_fb.png"  alt="" width="25" ></a></td>
                        <td  align="left" width="20"></td>	
                        <td align="left" width="25" valign="middle"><a href="https://twitter.com/AnalyticsSteps" target="_blank"><img src="https://analyticssteps.com/backend/media/mailer-images/icn_tw.png"  alt="" width="25" ></a></td>
                        <td  align="left" width="20"></td>	
                        <td align="left" width="25" valign="middle"><a href="https://www.linkedin.com/company/analytics-steps/" target="_blank"><img src="https://analyticssteps.com/backend/media/mailer-images/icn_lnk.png"  alt="" width="25" ></a></td>
                        
                        
                            
                        <td height="25" align="right" valign="middle"><img src="https://analyticssteps.com/backend/media/mailer-images/icn_web.png" height="15" alt="" style="margin-top:3px; line-height: 25px;"></td>
                        <td align="right" width="164" valign="middle"><a href="https://www.analyticssteps.com" target="_blank" style="line-height: 25px; font-family: Arial;font-size: 14px;font-weight:500; color: #ffffff;text-decoration: none;padding-left: 5px;"> www.analyticssteps.com</a></td>	
                        <td align="right" width="20"></td>
                            
                        </tr>
                        </table>
                            
                        </td></tr>
                              
                          </tbody>
                        </table>
                        </td>
                            </tr>
                          </tbody>
                        </table>
                        
                        </body>
                        </html>"""
    return content

def newsletter_email_temp(title, email_data):

    content = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml"><head>
    <title>Analytics Steps  | """ + title + """ </title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0"/>
    </head>
    <body>
    """ + email_data  + """
    </body>
    </html>
    """
    return content