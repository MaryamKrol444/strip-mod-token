"""Create original, non-explicit editorial diagrams. No platform screenshots."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'images'
OUT.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(size, bold=False): return ImageFont.truetype(BOLD if bold else FONT, size)
BG='#eeece5'; INK='#172523'; MUTED='#485953'; GREEN='#c8e4d3'; RED='#a63829'; DARK='#192b27'
SPECS = {
'home-access': ('THE FREE / PAID BOUNDARY', 'One interface. Separate decisions.', [('01  BROWSE', 'Public listings', 'Check age + location'), ('02  WATCH', 'Public broadcasts', 'No purchase required'), ('03  DECIDE', 'Tips / private / tickets', 'Check the token price')]),
'home-budget': ('FOLLOW THE MONEY', 'Turn tokens back into a cash amount.', [('PACKAGE', 'Cash / credited tokens', '= cost per token'), ('FEATURE', 'Unit cost x room rate', '= cash per minute'), ('VISIT', 'Minute cost x duration', '= planned spending')]),
'home-boundary': ('A ZERO-SPEND VISIT', 'Free viewing is a complete choice.', [('BEFORE', 'No payment method', 'Choose a time limit'), ('DURING', 'Public viewing only', 'Decline paid prompts'), ('AFTER', 'End your visit', 'Review shared devices')]),
'home-offers': ('CHANCE IS NOT A GUARANTEE', 'Account creation does not equal a prize.', [('ACCOUNT', 'Verify your email', 'Eligibility is not a win'), ('DRAW', 'Official selection', 'No guaranteed outcome'), ('CLAIM', 'Follow official terms', 'Check the time limit')]),
'home-checklist': ('THE FIRST-VISIT CHECK', 'Make the boundaries visible.', [('ACCESS', 'Age + official domain', 'Respect local rules'), ('PRIVACY', 'Camera + notifications', 'Keep identity separate'), ('COST', 'Public or paid?', 'Read before confirming')]),
'generator-ledger': ('THE SCREEN IS NOT THE LEDGER', 'A local number cannot authorize a credit.', [('CLIENT', 'Displays a balance', 'Can show a fake number'), ('SERVICE', 'Authorizes spending', 'Checks account records'), ('EVIDENCE', 'Official history', 'Not an animated counter')]),
'generator-funnel': ('ANATOMY OF A FALSE PROMISE', 'Warning patterns, not instructions.', [('THE HOOK', 'An invented balance', 'A progress bar proves nothing'), ('THE WALL', 'One more task', 'Surveys / payment requests'), ('THE COST', 'Your data or device', 'Leave before submitting')]),
'generator-redflags': ('RECOGNIZE THE PATTERN', 'Illustrative scam mockup. Not a real service.', [('FALSE CLAIM', 'Guaranteed credits', 'No official transaction'), ('DATA REQUEST', 'Password or code', 'Never share either'), ('INSTALL PROMPT', 'Untrusted software', 'Do not download')]),
'generator-recovery': ('RECOVERY, IN THE RIGHT ORDER', 'Match the response to the exposure.', [('ACCOUNT', 'Use a clean device', 'Change reused passwords'), ('DEVICE', 'Remove + scan', 'Review permissions'), ('PAYMENT', 'Check statements', 'Contact your provider')]),
'generator-proof': ('WHAT COUNTS AS EVIDENCE?', 'Keep the official account as the reference.', [('NOT PROOF', 'A success animation', 'Publisher controls the screen'), ('CHECK', 'Official token history', 'Look for a real credit'), ('ESCALATE', 'Official support', 'Keep credentials private')]),
'live-map': ('FOUR ROOM FORMATS', 'Audience and charging model are separate.', [('PUBLIC', 'Shared viewing', 'Tips are separate'), ('PRIVATE / SPY', 'Participant / spectator', 'Read live time-based rate'), ('TICKET / GROUP', 'Shared paid access', 'Fixed or timed? Check first')]),
'live-private': ('PRIVATE DOES NOT MEAN INVISIBLE', 'Read permissions before starting.', [('AUDIENCE', 'Are spectators allowed?', 'Check the room mode'), ('RECORDING', 'What do the terms say?', 'Capture can still happen'), ('EXIT', 'Find the stop control', 'Do not rely on closing a tab')]),
'live-ticket': ('FIXED ADMISSION OR TIMED ACCESS?', 'The group label does not answer the price question.', [('TICKET', 'Displayed entry price', 'Check event conditions'), ('GROUP', 'Read charging model', 'It may be time-based'), ('COMPARE', 'Same planned outcome', 'Not token numbers alone')]),
'live-camera': ('YOUR CAMERA. YOUR DECISION.', 'A privacy check before sharing.', [('FRAME', 'Neutral surroundings', 'Remove identifying details'), ('AUDIO', 'Choose the microphone', 'Check nearby conversations'), ('PERMISSIONS', 'Know the recipients', 'Revoke access afterward')]),
'live-quality': ('PLAYBACK WITHOUT THE GUESSWORK', 'Test before you enter a paid feature.', [('SOURCE', 'Performer connection', 'Affects the original stream'), ('DELIVERY', 'Network + other tabs', 'Reduce competing traffic'), ('DEVICE', 'Browser + decoding', 'Use supported software')]),
'sites-compare': ('THREE SITES. ONE FAIR METHOD.', 'Compare the same task across separate services.', [('STRIPCHAT', 'Check public access', 'Record live conditions'), ('CHATURBATE', 'Check public access', 'Record live conditions'), ('BONGACAMS', 'Check public access', 'Record live conditions')]),
'sites-math': ('CHEAPER TOKEN ≠ CHEAPER MINUTE', 'Illustration only. Not platform prices.', [('EXAMPLE A', '€0.10 x 20 tokens', '€2.00 per minute'), ('EXAMPLE B', '€0.08 x 30 tokens', '€2.40 per minute'), ('THE LESSON', 'Compare the outcome', 'Include all relevant fees')]),
'sites-payment': ('A PAYMENT HAS MORE THAN A PRICE', 'The official checkout is your transaction reference.', [('TOTAL', 'Currency + fees', 'Use the final amount'), ('METHOD', 'Provider + availability', 'Check your own account'), ('RECORD', 'Receipt + reference', 'Never store security codes')]),
'sites-privacy': ('FOUR LAYERS OF PRIVACY', 'No single switch covers all of them.', [('IDENTITY', 'Username + messages', 'Avoid offline linkage'), ('ACCOUNT', 'Password + recovery', 'Use unique credentials'), ('LOCAL / FINANCIAL', 'Screens + provider records', 'Incognito is not anonymity')]),
'sites-decision': ('FREE FIRST. FUND LATER, IF AT ALL.', 'A comparison can end without a purchase.', [('BROWSE', 'Test public rooms', 'Use the same device'), ('COMPARE', 'Fit + price + privacy', 'Reject unclear conditions'), ('DECIDE', 'One affordable plan', 'No deposit is also a decision')]),
}

def create(key, spec):
    title, subtitle, cards = spec
    im=Image.new('RGB', (1200,650), BG); d=ImageDraw.Draw(im)
    d.rectangle((0,0,1200,9), fill=RED)
    d.text((48,40),'OPENROOM  /  VISUAL NOTES',font=font(16,True),fill=MUTED)
    d.text((48,95),title,font=font(30,True),fill=INK)
    d.text((48,148),subtitle,font=font(21),fill=MUTED)
    for i,(label,main,sub) in enumerate(cards):
        x=48+i*374
        d.rounded_rectangle((x,218,x+355,526),radius=14,fill=DARK if i==1 else '#ffffff')
        fg='#f6f5ef' if i==1 else INK
        accent=GREEN if i==1 else RED
        d.ellipse((x+24,246,x+66,288),fill=accent)
        d.text((x+38,252),str(i+1),font=font(18,True),fill=DARK if i==1 else '#ffffff')
        d.text((x+24,316),label,font=font(16,True),fill=accent)
        # Fit text to width without ellipsis.
        size=23
        while d.textlength(main,font=font(size,True))>307: size-=1
        d.text((x+24,369),main,font=font(size,True),fill=fg)
        size=17
        while d.textlength(sub,font=font(size))>307: size-=1
        d.text((x+24,416),sub,font=font(size),fill=fg)
        d.line((x+24,478,x+328,478),fill=accent,width=2)
    d.text((48,578),'EDITORIAL ILLUSTRATION  ·  NOT A PLATFORM SCREENSHOT',font=font(16),fill=MUTED)
    d.text((1060,578),'18+',font=font(19,True),fill=RED)
    im.save(OUT / f'{key}.webp','WEBP',quality=86,method=6)

if __name__=='__main__':
    for key,spec in SPECS.items(): create(key,spec)
    # Social preview is original editorial art, with no adult imagery.
    im=Image.new('RGB',(1200,630),DARK); d=ImageDraw.Draw(im)
    d.text((75,65),'OPENROOM / INDEPENDENT FIELD NOTES',font=font(23,True),fill=GREEN)
    d.text((75,190),'Clear guides.',font=font(88,True),fill='#f6f5ef')
    d.text((75,300),'No false promises.',font=font(70,True),fill='#f6f5ef')
    d.text((75,510),'Free access · Live rooms · Token safety · 18+ only',font=font(25),fill=GREEN)
    im.save(OUT/'social.webp','WEBP',quality=88)
    print(f'Created {len(SPECS)+1} WebP illustrations')
