import random
import string

def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

message = '''<table style="background-color:#fff;margin:5% auto;width:100%;max-width:600px" cellspacing="0" cellpadding="0" border="0" bgcolor="#fff" align="center">

	<tbody><tr>
		<td>
			<table style="padding:10px 15px;font-size:14px" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#F96C00" align="center">
				<tbody><tr>
					<td style="padding:5px 0 0" width="60%" align="center">
						<span style="font-family:Roboto,RobotoDraft,Helvetica,Arial,sans-serif;color:#fff">RESET PASSWORD</span>
					</td>
				</tr>
			</tbody></table>
		</td>
	</tr>
	<tr>
		<td style="padding:25px 15px 10px">
			<table width="100%">
				<tbody><tr>
					<td>
						<h1 style="font-family:Roboto,RobotoDraft,Helvetica,Arial,sans-serif;margin:0;font-size:16px;font-weight:bold;line-height:24px;color:rgba(0,0,0,0.70)">Hello {},</h1>
					</td>
				</tr>
				<tr>
					<td>
						<p style="font-family:Roboto,RobotoDraft,Helvetica,Arial,sans-serif;margin:0;font-size:16px;line-height:24px;color:rgba(0,0,0,0.70)">You just tell me that you forgot your password, so here is the new one: {}<br>
                            Don't forget to change it after, you just don't want your password to be so hard to remember right? If you need any help, please don't hestitate to get in touch at this e-mail or our CEO at daffa@alterra.id<br></p>
					</td>
                </tr>
                <tr>
                    <td>
                        <h1 style="font-family:Roboto,RobotoDraft,Helvetica,Arial,sans-serif;margin:0;font-size:16px;font-weight:bold;line-height:24px;color:rgba(0,0,0,0.70)">Happy Teesigning!</h1>
                    </td>
                </tr>
			</tbody></table>
		</td>
	</tr>
</tbody></table>'''