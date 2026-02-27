import { useState, useEffect, useRef, useCallback } from "react";

// ── DATA ──
const AUTHOR = "Mehak Sharma";

const DESTINATIONS = {
  paris:     { country:"France",   emoji:"🗼", vibe:"Romantic, artsy, café culture",             budget:{hostel:45,food:25,transport:10,activities:15} },
  tokyo:     { country:"Japan",    emoji:"🗾", vibe:"Futuristic, food heaven, anime & culture",  budget:{hostel:35,food:20,transport:12,activities:18} },
  barcelona: { country:"Spain",    emoji:"🏖️", vibe:"Beach, tapas, Gaudí, nightlife",            budget:{hostel:30,food:20,transport:8, activities:12} },
  bangkok:   { country:"Thailand", emoji:"🛕", vibe:"Street food, temples, vibrant chaos",       budget:{hostel:12,food:8, transport:5, activities:10} },
  lisbon:    { country:"Portugal", emoji:"🌊", vibe:"Laid-back, stunning views, budget-friendly",budget:{hostel:25,food:15,transport:7, activities:10} },
};

const SUGGESTIONS = [
  { icon:"🍜", text:"What's the best cheap food to try in Tokyo as a student?" },
  { icon:"💰", text:"How do I travel from Paris to Barcelona on a tight budget?" },
  { icon:"🏠", text:"What should I look for when booking a hostel in Bangkok?" },
  { icon:"🧳", text:"What should I pack for a 7-day trip to Lisbon in October?" },
  { icon:"🎒", text:"Give me 5 money-saving tips for backpacking Europe." },
  { icon:"🗺️", text:"What are the most underrated hidden gems in Barcelona?" },
];

const INTERESTS = ["Food & Cuisine","History & Culture","Nightlife","Nature","Art & Museums","Architecture","Street Markets","Photography","Adventure Sports","Budget Shopping"];

const CHAT_SYSTEM = `You are TravelX AI, an expert student travel companion built by ${AUTHOR}. You specialize in budget travel, backpacking, student discounts, hidden gems, and practical travel advice. You're friendly, conversational, and concise. Give specific, actionable advice. Use emojis naturally. Focus on budget-conscious tips. Keep responses to 3-5 short paragraphs max.`;

// ── CLAUDE API ──
async function callClaude(messages, system = "", maxTokens = 1000) {
  const body = { model: "claude-sonnet-4-20250514", max_tokens: maxTokens, messages };
  if (system) body.system = system;
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`API ${res.status}`);
  const data = await res.json();
  return data.content.map(b => b.text || "").join("");
}

// ── STARFIELD CANVAS ──
function Starfield() {
  const canvasRef = useRef(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    let animId, stars = [], shooting = [], t = 0;
    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      stars = Array.from({ length: Math.floor((canvas.width * canvas.height) / 4200) }, () => ({
        x: Math.random() * canvas.width, y: Math.random() * canvas.height,
        r: Math.random() * 1.3 + 0.2, a: Math.random() * 0.7 + 0.2,
        ts: Math.random() * 0.018 + 0.004, tp: Math.random() * Math.PI * 2,
        c: Math.random() < 0.12 ? "#b39ddb" : Math.random() < 0.08 ? "#40c4ff" : "#e8eaf6",
      }));
    };
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      [
        { x: canvas.width*0.75, y: canvas.height*0.15, r: 300, c: "rgba(124,106,255,0.06)" },
        { x: canvas.width*0.15, y: canvas.height*0.5,  r: 240, c: "rgba(64,196,255,0.04)"  },
        { x: canvas.width*0.5,  y: canvas.height*0.8,  r: 360, c: "rgba(179,157,219,0.03)" },
      ].forEach(n => {
        const g = ctx.createRadialGradient(n.x,n.y,0,n.x,n.y,n.r);
        g.addColorStop(0,n.c); g.addColorStop(1,"transparent");
        ctx.fillStyle=g; ctx.beginPath(); ctx.arc(n.x,n.y,n.r,0,Math.PI*2); ctx.fill();
      });
      stars.forEach(s => {
        const tw = Math.sin(t*s.ts+s.tp)*0.3+0.7;
        ctx.beginPath(); ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
        ctx.fillStyle=s.c; ctx.globalAlpha=s.a*tw; ctx.fill(); ctx.globalAlpha=1;
      });
      if (Math.random()<0.004) shooting.push({ x:Math.random()*canvas.width, y:Math.random()*canvas.height*0.5, len:Math.random()*100+50, spd:Math.random()*5+4, a:1, ang:Math.PI/4+(Math.random()-.5)*0.3, life:1 });
      shooting = shooting.filter(s => s.life > 0);
      shooting.forEach(s => {
        ctx.save(); ctx.translate(s.x,s.y); ctx.rotate(s.ang);
        const g=ctx.createLinearGradient(-s.len,0,0,0);
        g.addColorStop(0,"transparent"); g.addColorStop(1,`rgba(255,255,255,${s.life*0.85})`);
        ctx.strokeStyle=g; ctx.lineWidth=1.5; ctx.globalAlpha=s.a;
        ctx.beginPath(); ctx.moveTo(-s.len,0); ctx.lineTo(0,0); ctx.stroke();
        ctx.globalAlpha=1; ctx.restore();
        s.x+=Math.cos(s.ang)*s.spd; s.y+=Math.sin(s.ang)*s.spd; s.life-=0.02; s.a=s.life;
      });
      t++; animId=requestAnimationFrame(draw);
    };
    resize(); draw();
    window.addEventListener("resize", resize);
    return () => { cancelAnimationFrame(animId); window.removeEventListener("resize", resize); };
  }, []);
  return <canvas ref={canvasRef} style={{ position:"fixed",inset:0,zIndex:0,pointerEvents:"none" }} />;
}

// ── TOAST ──
function Toast({ msg, show }) {
  return (
    <div style={{
      position:"fixed",bottom:28,right:28,zIndex:1000,
      background:"#0d0d22",color:"#e8eaf6",padding:"11px 18px",
      borderRadius:4,fontSize:12,borderLeft:"3px solid #7c6aff",
      fontFamily:"'Space Mono',monospace",
      transform: show ? "translateX(0)" : "translateX(140%)",
      transition:"transform .4s cubic-bezier(.16,1,.3,1)",
    }}>{msg}</div>
  );
}

// ── TYPING INDICATOR ──
function TypingDots() {
  return (
    <div style={{ display:"flex",gap:5,padding:"12px 15px",background:"rgba(124,106,255,.08)",border:"1px solid rgba(124,106,255,.12)",borderRadius:"2px 10px 10px 10px",width:"fit-content" }}>
      {[0,200,400].map(d => (
        <div key={d} style={{
          width:7,height:7,borderRadius:"50%",background:"#7c6aff",
          animation:"typing 1.2s infinite",animationDelay:`${d}ms`
        }}/>
      ))}
    </div>
  );
}

// ── MAIN APP ──
export default function TravelXAI() {
  // Section refs
  const chatRef     = useRef(null);
  const itinRef     = useRef(null);
  const budgetRef   = useRef(null);
  const destRef     = useRef(null);

  // Toast
  const [toastMsg, setToastMsg]   = useState("");
  const [toastShow, setToastShow] = useState(false);
  const showToast = (msg) => { setToastMsg(msg); setToastShow(true); setTimeout(()=>setToastShow(false),3000); };

  // Chat state
  const [chatHistory, setChatHistory] = useState([]);
  const [chatInput,   setChatInput]   = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [messages, setMessages] = useState([
    { role:"ai", text:"Hey explorer! 🌍 I'm your AI travel buddy built by Mehak Sharma. Ask me anything — best street food in Tokyo, how to get from Paris to Barcelona on a budget, what to pack for Bangkok, or anything travel-related. Let's plan your adventure!" }
  ]);
  const chatEndRef = useRef(null);
  useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior:"smooth" }); }, [messages, chatLoading]);

  const sendMessage = useCallback(async (text) => {
    const msg = (text || chatInput).trim();
    if (!msg || chatLoading) return;
    setChatInput("");
    setMessages(prev => [...prev, { role:"user", text:msg }]);
    const newHistory = [...chatHistory, { role:"user", content:msg }];
    setChatHistory(newHistory);
    setChatLoading(true);
    try {
      const reply = await callClaude(newHistory, CHAT_SYSTEM, 800);
      setMessages(prev => [...prev, { role:"ai", text:reply }]);
      setChatHistory(prev => [...prev, { role:"assistant", content:reply }]);
    } catch {
      setMessages(prev => [...prev, { role:"ai", text:"⚠️ Couldn't reach the AI right now. Please try again in a moment." }]);
    }
    setChatLoading(false);
  }, [chatInput, chatHistory, chatLoading]);

  // Itinerary state
  const [itinDest,    setItinDest]    = useState("");
  const [itinDays,    setItinDays]    = useState("5");
  const [itinBudget,  setItinBudget]  = useState("balanced ($40–$80/day)");
  const [itinSpecial, setItinSpecial] = useState("");
  const [itinInterests, setItinInterests] = useState([]);
  const [itinResult,  setItinResult]  = useState(null);
  const [itinLoading, setItinLoading] = useState(false);

  const toggleInterest = (i) => setItinInterests(prev => prev.includes(i) ? prev.filter(x=>x!==i) : [...prev,i]);

  const generateItinerary = async () => {
    if (!itinDest) { showToast("⚠️ Please select a destination!"); return; }
    setItinLoading(true); setItinResult(null);
    const iText = itinInterests.length ? `Interests: ${itinInterests.join(", ")}.` : "";
    const sText = itinSpecial ? `Special requests: ${itinSpecial}.` : "";
    const prompt = `Create a detailed ${itinDays}-day itinerary for a student visiting ${itinDest} on a ${itinBudget} budget. ${iText} ${sText}\n\nFormat with:\n- Brief intro (2 sentences)\n- Each day: DAY N: [Theme], then Morning / Afternoon / Evening with specific places and USD costs\n- 3 practical student tips at the end\n- Estimated total budget summary\n\nBe specific with real place names and realistic USD cost estimates. Focus on authentic local experiences.`;
    try {
      const reply = await callClaude([{ role:"user", content:prompt }],
        `You are TravelX AI, an expert student travel planner built by ${AUTHOR}. Create practical, budget-focused itineraries with specific places and realistic costs.`, 1200);
      setItinResult(reply);
      showToast("✨ Itinerary generated!");
    } catch {
      showToast("⚠️ Generation failed. Please try again.");
    }
    setItinLoading(false);
  };

  // Budget AI state
  const [baDest,    setBaDest]    = useState("");
  const [baBudget,  setBaBudget]  = useState("");
  const [baDays,    setBaDays]    = useState("");
  const [baStyle,   setBaStyle]   = useState("balanced");
  const [baConcern, setBaConcern] = useState("overall trip feasibility");
  const [baResult,  setBaResult]  = useState(null);
  const [baLoading, setBaLoading] = useState(false);

  const analyzeBudget = async () => {
    if (!baDest || !baBudget || !baDays) { showToast("⚠️ Please fill all fields!"); return; }
    setBaLoading(true); setBaResult(null);
    const prompt = `A student wants to visit ${baDest} for ${baDays} days with $${baBudget} USD total budget. Travel style: ${baStyle}. Biggest concern: ${baConcern}.\n\nProvide:\n1. Is this budget realistic? (be honest)\n2. Daily breakdown: accommodation, food, transport, activities (with USD amounts)\n3. Top 3 ways to save money in this specific destination\n4. Where it's worth spending a bit more\n5. Bare minimum vs comfortable budget comparison\n6. Hidden costs to watch out for\n\nBe specific, honest, and student-focused. Use USD amounts throughout.`;
    try {
      const reply = await callClaude([{ role:"user", content:prompt }],
        `You are TravelX AI, a student travel budget expert built by ${AUTHOR}. Give honest, specific, actionable budget analysis with real cost estimates.`, 900);
      setBaResult(reply);
      showToast("💰 Budget analysis ready!");
    } catch {
      showToast("⚠️ Analysis failed. Please try again.");
    }
    setBaLoading(false);
  };

  const scrollTo = (ref) => ref.current?.scrollIntoView({ behavior:"smooth" });

  // ── STYLES ──
  const css = `
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=Space+Mono:wght@400;700&display=swap');
    *{box-sizing:border-box;margin:0;padding:0;}
    :root{--ink:#e8eaf6;--paper:#06060f;--cream:#0d0d1f;--accent:#7c6aff;--accent2:#40c4ff;--gold:#b39ddb;--muted:#8888aa;--success:#4caf88;}
    body{font-family:'DM Sans',sans-serif;background:#06060f;color:#e8eaf6;overflow-x:hidden;cursor:none;}
    @keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.7)}}
    @keyframes float{0%,100%{transform:translateY(-50%) translateX(0)}50%{transform:translateY(-50%) translateX(-10px)}}
    @keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
    @keyframes msgIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
    @keyframes typing{0%,60%,100%{transform:translateY(0);opacity:.4}30%{transform:translateY(-6px);opacity:1}}
    @keyframes spin{to{transform:rotate(360deg)}}
    @keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
    ::-webkit-scrollbar{width:4px} ::-webkit-scrollbar-thumb{background:rgba(124,106,255,.3);border-radius:2px}
    input,select,textarea{font-family:'DM Sans',sans-serif;}
    select option{background:#0d0d22;}
  `;

  const S = {
    // Layout
    wrap:   { position:"relative", minHeight:"100vh", background:"#06060f" },
    // Header
    header: { position:"fixed",top:0,left:0,right:0,zIndex:100,display:"flex",alignItems:"center",justifyContent:"space-between",padding:"18px 48px",background:"rgba(6,6,15,.85)",backdropFilter:"blur(20px)",borderBottom:"1px solid rgba(124,106,255,.12)" },
    logo:   { fontFamily:"'Bebas Neue',sans-serif",fontSize:26,letterSpacing:".06em",display:"flex",alignItems:"center",gap:6,color:"#e8eaf6" },
    aiBadge:{ fontFamily:"'Space Mono',monospace",fontSize:9,background:"linear-gradient(135deg,#7c6aff,#40c4ff)",color:"white",padding:"2px 8px",borderRadius:20,letterSpacing:".1em",marginLeft:6 },
    nav:    { display:"flex",gap:24,alignItems:"center" },
    navA:   { fontFamily:"'Space Mono',monospace",fontSize:10,letterSpacing:".12em",textTransform:"uppercase",color:"rgba(232,234,246,.4)",textDecoration:"none",cursor:"none" },
    navBtn: { fontFamily:"'Space Mono',monospace",fontSize:10,letterSpacing:".1em",textTransform:"uppercase",background:"linear-gradient(135deg,#7c6aff,#40c4ff)",color:"white",border:"none",padding:"8px 18px",borderRadius:2,cursor:"none",boxShadow:"0 0 16px rgba(124,106,255,.3)" },
    // Section
    sec:    { padding:"90px 48px",position:"relative",zIndex:1 },
    label:  { fontFamily:"'Space Mono',monospace",fontSize:10,letterSpacing:".2em",textTransform:"uppercase",color:"#7c6aff",marginBottom:14 },
    h2:     { fontFamily:"'Bebas Neue',sans-serif",fontSize:"clamp(40px,5vw,68px)",lineHeight:1,letterSpacing:".02em",marginBottom:14 },
    intro:  { color:"#8888aa",fontSize:15,maxWidth:520,marginBottom:44,lineHeight:1.7 },
    // Inputs
    formGrp:{ marginBottom:20 },
    lbl:    { display:"block",fontFamily:"'Space Mono',monospace",fontSize:10,letterSpacing:".14em",textTransform:"uppercase",color:"#8888aa",marginBottom:8 },
    inp:    { width:"100%",padding:"11px 13px",border:"1.5px solid rgba(124,106,255,.14)",borderRadius:2,fontSize:14,background:"rgba(255,255,255,.04)",color:"#e8eaf6",outline:"none",transition:"border-color .2s",appearance:"none" },
    // Buttons
    genBtn: { width:"100%",fontFamily:"'Bebas Neue',sans-serif",fontSize:18,letterSpacing:".08em",background:"linear-gradient(135deg,#7c6aff,#40c4ff)",color:"white",border:"none",padding:15,cursor:"none",borderRadius:2,marginTop:8,boxShadow:"0 0 22px rgba(124,106,255,.35)",transition:"all .2s" },
    sendBtn:{ background:"linear-gradient(135deg,#7c6aff,#40c4ff)",border:"none",borderRadius:4,width:42,height:42,display:"flex",alignItems:"center",justifyContent:"center",cursor:"none",flexShrink:0,fontSize:15,boxShadow:"0 0 14px rgba(124,106,255,.3)" },
  };

  return (
    <>
      <style>{css}</style>
      <Toast msg={toastMsg} show={toastShow} />
      <Starfield />

      {/* Custom cursor */}
      <CustomCursor />

      {/* HEADER */}
      <header style={S.header}>
        <div style={S.logo}>
          Travel<span style={{color:"#7c6aff"}}>X</span>
          <span style={S.aiBadge}>AI</span>
        </div>
        <nav style={S.nav}>
          {[["AI Assistant","chatRef"],["Itinerary","itinRef"],["Budget AI","budgetRef"],["Destinations","destRef"]].map(([name,ref])=>(
            <a key={name} style={S.navA} onClick={()=>scrollTo({chatRef,itinRef,budgetRef,destRef}[ref])} href="#">{name}</a>
          ))}
          <button style={S.navBtn} onClick={()=>scrollTo(chatRef)}>✦ Ask AI</button>
        </nav>
      </header>

      {/* HERO */}
      <section style={{ minHeight:"100vh",display:"flex",alignItems:"center",padding:"120px 48px 80px",position:"relative",overflow:"hidden",zIndex:1 }}>
        <div style={{ position:"absolute",inset:0,background:"radial-gradient(ellipse 70% 60% at 75% 40%,rgba(124,106,255,.15) 0%,transparent 65%),radial-gradient(ellipse 50% 50% at 20% 65%,rgba(64,196,255,.08) 0%,transparent 60%)" }}/>
        <div style={{ position:"absolute",inset:0,backgroundImage:"linear-gradient(rgba(124,106,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(124,106,255,.05) 1px,transparent 1px)",backgroundSize:"60px 60px",maskImage:"linear-gradient(to bottom,transparent,black 30%,black 70%,transparent)" }}/>
        <div style={{ position:"relative",maxWidth:650 }}>
          <div style={{ display:"inline-flex",alignItems:"center",gap:8,fontFamily:"'Space Mono',monospace",fontSize:10,letterSpacing:".15em",textTransform:"uppercase",color:"#40c4ff",background:"rgba(64,196,255,.08)",padding:"6px 14px",borderRadius:2,marginBottom:24,border:"1px solid rgba(64,196,255,.2)",animation:"fadeUp .7s ease forwards" }}>
            <span style={{ width:7,height:7,background:"#40c4ff",borderRadius:"50%",animation:"pulse 2s infinite",display:"inline-block" }}/>
            Powered by {AUTHOR}
          </div>
          <h1 style={{ fontFamily:"'Bebas Neue',sans-serif",fontSize:"clamp(68px,9vw,120px)",lineHeight:.92,letterSpacing:".01em",marginBottom:24,animation:"fadeUp .7s .15s ease both" }}>
            TRAVEL<br/><span style={{ color:"#7c6aff",textShadow:"0 0 40px rgba(124,106,255,.5)" }}>SMARTER</span><br/>WITH AI
          </h1>
          <p style={{ fontSize:17,lineHeight:1.7,color:"#8888aa",maxWidth:460,marginBottom:40,animation:"fadeUp .7s .3s ease both" }}>
            Your personal AI travel companion. Get custom itineraries, real budget analysis, and instant answers — built for student explorers.
          </p>
          <div style={{ display:"flex",gap:14,flexWrap:"wrap",animation:"fadeUp .7s .45s ease both" }}>
            <button onClick={()=>scrollTo(chatRef)} style={{ fontFamily:"'Space Mono',monospace",fontSize:11,letterSpacing:".1em",textTransform:"uppercase",background:"linear-gradient(135deg,#7c6aff,#40c4ff)",color:"white",padding:"15px 32px",border:"none",borderRadius:2,cursor:"none",boxShadow:"0 0 24px rgba(124,106,255,.4)" }}>✦ Chat with AI</button>
            <button onClick={()=>scrollTo(itinRef)} style={{ fontFamily:"'Space Mono',monospace",fontSize:11,letterSpacing:".1em",textTransform:"uppercase",background:"transparent",color:"#e8eaf6",padding:"15px 32px",border:"1.5px solid rgba(124,106,255,.35)",borderRadius:2,cursor:"none" }}>Generate Itinerary</button>
          </div>
        </div>
        {/* Floating pills */}
        <div style={{ position:"absolute",right:48,top:"50%",display:"flex",flexDirection:"column",gap:10,animation:"float 6s ease-in-out infinite" }}>
          {[["AI","Generative\nIntelligence",""],["5","Destinations\ncovered","✈️"],["∞","Custom\nitineraries","⚡"]].map(([num,lbl,icon])=>(
            <div key={num} style={{ background:"rgba(13,13,31,.92)",borderRadius:8,padding:"14px 20px",boxShadow:"0 4px 24px rgba(0,0,0,.4),0 0 0 1px rgba(124,106,255,.14)",display:"flex",gap:12,alignItems:"center",backdropFilter:"blur(10px)" }}>
              {icon && <span style={{fontSize:20}}>{icon}</span>}
              <div><div style={{ fontFamily:"'Bebas Neue',sans-serif",fontSize:28,color:"#7c6aff",lineHeight:1,textShadow:"0 0 14px rgba(124,106,255,.5)" }}>{num}</div></div>
              <div style={{ fontSize:11,color:"#8888aa",lineHeight:1.4,whiteSpace:"pre" }}>{lbl}</div>
            </div>
          ))}
        </div>
      </section>

      {/* AI CHAT */}
      <section ref={chatRef} style={{ ...S.sec, background:"#0d0d1f" }}>
        <div style={S.label}>✦ Generative AI</div>
        <h2 style={S.h2}>CHAT WITH YOUR<br/>AI TRAVEL BUDDY</h2>
        <p style={S.intro}>Ask anything about travel — budgets, hidden gems, visa tips, packing advice. Powered by Claude AI, built by {AUTHOR}.</p>
        <div style={{ display:"grid",gridTemplateColumns:"1fr 1.2fr",gap:32,alignItems:"start" }}>
          {/* Suggestions */}
          <div>
            <div style={{ fontFamily:"'Space Mono',monospace",fontSize:10,letterSpacing:".15em",textTransform:"uppercase",color:"#8888aa",marginBottom:10 }}>Try asking…</div>
            <div style={{ display:"flex",flexDirection:"column",gap:8 }}>
              {SUGGESTIONS.map((s,i) => (
                <button key={i} onClick={()=>sendMessage(s.text)} style={{ background:"rgba(124,106,255,.06)",border:"1px solid rgba(124,106,255,.15)",borderRadius:4,padding:"12px 16px",cursor:"none",fontSize:13,color:"rgba(232,234,246,.75)",lineHeight:1.5,textAlign:"left",transition:"all .2s" }}
                  onMouseEnter={e=>{e.currentTarget.style.background="rgba(124,106,255,.15)";e.currentTarget.style.borderColor="#7c6aff";}}
                  onMouseLeave={e=>{e.currentTarget.style.background="rgba(124,106,255,.06)";e.currentTarget.style.borderColor="rgba(124,106,255,.15)";}}>
                  <span style={{marginRight:8}}>{s.icon}</span>{s.text}
                </button>
              ))}
            </div>
            <div style={{ marginTop:24,display:"flex",flexDirection:"column",gap:9 }}>
              {["Personalized to your budget & style","Real local tips, not tourist fluff","Instant answers powered by Claude AI","Understands student travel context"].map(f => (
                <div key={f} style={{ display:"flex",alignItems:"center",gap:10,fontSize:13,color:"#8888aa" }}>
                  <div style={{ width:6,height:6,borderRadius:"50%",background:"linear-gradient(135deg,#7c6aff,#40c4ff)",flexShrink:0 }}/>
                  {f}
                </div>
              ))}
            </div>
          </div>
          {/* Chat box */}
          <div style={{ background:"#08081a",borderRadius:6,border:"1px solid rgba(124,106,255,.12)",overflow:"hidden",boxShadow:"0 8px 40px rgba(0,0,0,.4)" }}>
            <div style={{ padding:"16px 22px",background:"rgba(124,106,255,.06)",borderBottom:"1px solid rgba(124,106,255,.1)",display:"flex",alignItems:"center",gap:10 }}>
              <div style={{ width:32,height:32,borderRadius:"50%",background:"linear-gradient(135deg,#7c6aff,#40c4ff)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:14,boxShadow:"0 0 12px rgba(124,106,255,.4)" }}>🤖</div>
              <div>
                <div style={{ fontFamily:"'Space Mono',monospace",fontSize:12,color:"#e8eaf6" }}>TravelX AI</div>
                <div style={{ fontSize:11,color:"#4caf88",display:"flex",alignItems:"center",gap:5 }}>
                  <span style={{ width:6,height:6,background:"#4caf88",borderRadius:"50%",display:"inline-block",animation:"pulse 2s infinite" }}/>
                  Online & ready
                </div>
              </div>
            </div>
            <div style={{ height:360,overflowY:"auto",padding:18,display:"flex",flexDirection:"column",gap:14 }}>
              {messages.map((m,i) => (
                <div key={i} style={{ display:"flex",gap:10,alignItems:"flex-start",flexDirection:m.role==="user"?"row-reverse":"row",animation:"msgIn .3s ease" }}>
                  <div style={{ width:28,height:28,borderRadius:"50%",flexShrink:0,display:"flex",alignItems:"center",justifyContent:"center",fontSize:12,background:m.role==="ai"?"linear-gradient(135deg,#7c6aff,#40c4ff)":"rgba(255,255,255,.08)",border:m.role==="user"?"1px solid rgba(255,255,255,.1)":"none" }}>
                    {m.role==="ai"?"🤖":"🧑"}
                  </div>
                  <div style={{ maxWidth:"82%",padding:"12px 16px",fontSize:13.5,lineHeight:1.65,borderRadius:m.role==="ai"?"2px 10px 10px 10px":"10px 2px 10px 10px",background:m.role==="ai"?"rgba(124,106,255,.08)":"linear-gradient(135deg,rgba(124,106,255,.25),rgba(64,196,255,.15))",border:m.role==="ai"?"1px solid rgba(124,106,255,.12)":"1px solid rgba(124,106,255,.2)",color:m.role==="ai"?"rgba(232,234,246,.88)":"#e8eaf6",whiteSpace:"pre-wrap" }}>
                    {m.text}
                  </div>
                </div>
              ))}
              {chatLoading && (
                <div style={{ display:"flex",gap:10,alignItems:"flex-start" }}>
                  <div style={{ width:28,height:28,borderRadius:"50%",background:"linear-gradient(135deg,#7c6aff,#40c4ff)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:12 }}>🤖</div>
                  <TypingDots/>
                </div>
              )}
              <div ref={chatEndRef}/>
            </div>
            <div style={{ padding:"14px 16px",borderTop:"1px solid rgba(124,106,255,.1)",background:"rgba(6,6,15,.6)",display:"flex",gap:10,alignItems:"flex-end" }}>
              <textarea value={chatInput} onChange={e=>setChatInput(e.target.value)}
                onKeyDown={e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();sendMessage();}}}
                placeholder="Ask me anything about travel…" rows={1}
                style={{ flex:1,background:"rgba(255,255,255,.04)",border:"1.5px solid rgba(124,106,255,.15)",borderRadius:4,padding:"11px 14px",fontSize:14,color:"#e8eaf6",resize:"none",minHeight:42,maxHeight:110,lineHeight:1.5,outline:"none" }}/>
              <button onClick={()=>sendMessage()} disabled={chatLoading} style={{ ...S.sendBtn,opacity:chatLoading?.4:1 }}>➤</button>
            </div>
          </div>
        </div>
      </section>

      {/* ITINERARY */}
      <section ref={itinRef} style={{ ...S.sec, background:"#06060f" }}>
        <div style={S.label}>✦ AI-Generated Plans</div>
        <h2 style={{ ...S.h2,color:"#e8eaf6" }}>GENERATE YOUR<br/>PERFECT ITINERARY</h2>
        <div style={{ display:"grid",gridTemplateColumns:"360px 1fr",gap:32,marginTop:44 }}>
          {/* Form */}
          <div style={{ background:"#0d0d22",padding:32,borderRadius:4,border:"1px solid rgba(124,106,255,.1)" }}>
            {[
              ["Destination", <select value={itinDest} onChange={e=>setItinDest(e.target.value)} style={S.inp}>
                <option value="">— Choose a city —</option>
                {Object.entries(DESTINATIONS).map(([k,d])=><option key={k} value={`${k.charAt(0).toUpperCase()+k.slice(1)}, ${d.country}`}>{d.emoji} {k.charAt(0).toUpperCase()+k.slice(1)}, {d.country}</option>)}
              </select>],
              ["Duration (days)", <input type="number" value={itinDays} onChange={e=>setItinDays(e.target.value)} min="1" max="30" style={S.inp}/>],
              ["Budget Level", <select value={itinBudget} onChange={e=>setItinBudget(e.target.value)} style={S.inp}>
                <option value="budget backpacker (under $40/day)">🎒 Budget Backpacker</option>
                <option value="balanced ($40–$80/day)">⚖️ Balanced</option>
                <option value="comfort seeker ($80+/day)">🌟 Comfort Seeker</option>
              </select>],
            ].map(([label,input])=>(
              <div key={label} style={S.formGrp}><label style={S.lbl}>{label}</label>{input}</div>
            ))}
            <div style={S.formGrp}>
              <label style={S.lbl}>Your Interests</label>
              <div style={{ display:"flex",flexWrap:"wrap",gap:7 }}>
                {INTERESTS.map(i=>(
                  <button key={i} onClick={()=>toggleInterest(i)} style={{ fontFamily:"'Space Mono',monospace",fontSize:9,letterSpacing:".08em",textTransform:"uppercase",padding:"6px 10px",border:"1px solid rgba(124,106,255,.14)",borderRadius:2,background:itinInterests.includes(i)?"rgba(124,106,255,.18)":"transparent",color:itinInterests.includes(i)?"#e8eaf6":"rgba(232,234,246,.45)",cursor:"none",borderColor:itinInterests.includes(i)?"#7c6aff":"rgba(124,106,255,.14)" }}>{i}</button>
                ))}
              </div>
            </div>
            <div style={S.formGrp}>
              <label style={S.lbl}>Special Requests (optional)</label>
              <input type="text" value={itinSpecial} onChange={e=>setItinSpecial(e.target.value)} placeholder="e.g. vegetarian food, no museums…" style={S.inp}/>
            </div>
            <button onClick={generateItinerary} disabled={itinLoading} style={{ ...S.genBtn,opacity:itinLoading?.6:1 }}>
              {itinLoading?"✦ GENERATING…":"✦ GENERATE WITH AI →"}
            </button>
          </div>
          {/* Output */}
          <div style={{ background:"#0a0a1e",borderRadius:4,border:"1px solid rgba(124,106,255,.1)",minHeight:480,display:"flex",alignItems:itinResult||itinLoading?"flex-start":"center",justifyContent:itinResult||itinLoading?"flex-start":"center",overflow:"hidden" }}>
            {!itinResult && !itinLoading && (
              <div style={{ textAlign:"center",color:"rgba(232,234,246,.18)",padding:40 }}>
                <div style={{ fontSize:50,marginBottom:12 }}>🗺️</div>
                <p style={{ fontFamily:"'Space Mono',monospace",fontSize:11,letterSpacing:".12em",textTransform:"uppercase" }}>Your AI itinerary will appear here</p>
              </div>
            )}
            {itinLoading && (
              <div style={{ display:"flex",flexDirection:"column",alignItems:"center",gap:18,padding:60,width:"100%" }}>
                <div style={{ width:44,height:44,border:"2px solid rgba(124,106,255,.15)",borderTopColor:"#7c6aff",borderRadius:"50%",animation:"spin 1s linear infinite" }}/>
                <p style={{ fontFamily:"'Space Mono',monospace",fontSize:11,color:"#8888aa",letterSpacing:".12em",textTransform:"uppercase",textAlign:"center" }}>AI is crafting your itinerary…<br/>this takes a few seconds</p>
              </div>
            )}
            {itinResult && !itinLoading && (
              <div style={{ width:"100%",padding:32 }}>
                <div style={{ display:"flex",alignItems:"flex-start",justifyContent:"space-between",marginBottom:20 }}>
                  <div>
                    <div style={{ fontFamily:"'Bebas Neue',sans-serif",fontSize:40,color:"#7c6aff",letterSpacing:".04em",lineHeight:1 }}>{itinDest.split(",")[0].toUpperCase()}</div>
                    <div style={{ fontSize:12,color:"#8888aa",marginTop:5 }}>{itinDays} days · {itinBudget}</div>
                  </div>
                  <div style={{ fontFamily:"'Space Mono',monospace",fontSize:9,textTransform:"uppercase",letterSpacing:".1em",background:"linear-gradient(135deg,#7c6aff,#40c4ff)",color:"white",padding:"3px 10px",borderRadius:20,whiteSpace:"nowrap" }}>✦ AI Generated</div>
                </div>
                <div style={{ fontSize:13.5,lineHeight:1.8,color:"rgba(232,234,246,.8)",whiteSpace:"pre-wrap" }}>
                  {itinResult.split("\n").map((line,i)=>{
                    if(/^DAY \d+/i.test(line)) return <div key={i} style={{ fontFamily:"'Bebas Neue',sans-serif",fontSize:20,color:"#40c4ff",letterSpacing:".06em",margin:"18px 0 6px" }}>{line}</div>;
                    if(line.startsWith("**")||line.startsWith("##")) return <div key={i} style={{ fontWeight:600,color:"#e8eaf6",marginTop:8 }}>{line.replace(/\*\*|##/g,"")}</div>;
                    return <div key={i}>{line}</div>;
                  })}
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* BUDGET AI */}
      <section ref={budgetRef} style={{ ...S.sec, background:"#0d0d1f" }}>
        <div style={S.label}>✦ Smart Budget Analysis</div>
        <h2 style={S.h2}>AI BUDGET<br/>ANALYZER</h2>
        <p style={S.intro}>Tell the AI your destination, budget, and travel style — it'll break down exactly how to make it work, where to save, and where it's worth splurging.</p>
        <div style={{ display:"grid",gridTemplateColumns:"1fr 1fr",gap:32 }}>
          {/* Form */}
          <div style={{ background:"#0d0d22",padding:32,borderRadius:4,border:"1px solid rgba(124,106,255,.1)" }}>
            {[
              ["Destination", <select value={baDest} onChange={e=>setBaDest(e.target.value)} style={S.inp}>
                <option value="">— Select destination —</option>
                {Object.entries(DESTINATIONS).map(([k,d])=><option key={k} value={k.charAt(0).toUpperCase()+k.slice(1)}>{d.emoji} {k.charAt(0).toUpperCase()+k.slice(1)}</option>)}
              </select>],
              ["Total Budget (USD)", <input type="number" value={baBudget} onChange={e=>setBaBudget(e.target.value)} placeholder="e.g. 800" min="50" style={S.inp}/>],
              ["Trip Duration (days)", <input type="number" value={baDays} onChange={e=>setBaDays(e.target.value)} placeholder="e.g. 7" min="1" max="60" style={S.inp}/>],
              ["Travel Style", <select value={baStyle} onChange={e=>setBaStyle(e.target.value)} style={S.inp}>
                <option value="budget backpacker">🎒 Budget Backpacker</option>
                <option value="balanced">⚖️ Balanced</option>
                <option value="comfort seeker">🌟 Comfort Seeker</option>
              </select>],
              ["Biggest Concern", <select value={baConcern} onChange={e=>setBaConcern(e.target.value)} style={S.inp}>
                <option value="accommodation costs">🏠 Accommodation costs</option>
                <option value="food expenses">🍜 Food expenses</option>
                <option value="transport within the city">🚌 Getting around</option>
                <option value="activities and sightseeing">🎭 Activities</option>
                <option value="overall trip feasibility">💰 Overall feasibility</option>
              </select>],
            ].map(([label,input])=>(
              <div key={label} style={S.formGrp}><label style={S.lbl}>{label}</label>{input}</div>
            ))}
            <button onClick={analyzeBudget} disabled={baLoading} style={{ ...S.genBtn,opacity:baLoading?.6:1 }}>
              {baLoading?"✦ ANALYZING…":"✦ ANALYZE MY BUDGET →"}
            </button>
          </div>
          {/* Result */}
          <div style={{ background:"#08081a",borderRadius:4,border:"1px solid rgba(124,106,255,.1)",padding:32,minHeight:380,display:"flex",flexDirection:"column" }}>
            <div style={{ fontFamily:"'Space Mono',monospace",fontSize:10,textTransform:"uppercase",letterSpacing:".15em",color:"#b39ddb",marginBottom:14,display:"flex",alignItems:"center",gap:8 }}>
              AI Budget Analysis
              <div style={{ flex:1,height:1,background:"rgba(255,255,255,.06)" }}/>
            </div>
            {!baResult && !baLoading && (
              <div style={{ flex:1,display:"flex",alignItems:"center",justifyContent:"center",color:"rgba(232,234,246,.16)",textAlign:"center" }}>
                <p style={{ fontFamily:"'Space Mono',monospace",fontSize:11,letterSpacing:".1em",textTransform:"uppercase",lineHeight:1.8 }}>Fill in the form to get<br/>your AI budget breakdown</p>
              </div>
            )}
            {baLoading && (
              <div style={{ flex:1,display:"flex",alignItems:"center",justifyContent:"center",gap:12,color:"#8888aa",fontSize:13 }}>
                <div style={{ width:20,height:20,border:"2px solid rgba(124,106,255,.2)",borderTopColor:"#7c6aff",borderRadius:"50%",animation:"spin 1s linear infinite" }}/>
                Analyzing your budget…
              </div>
            )}
            {baResult && !baLoading && (
              <div style={{ fontSize:13.5,lineHeight:1.8,color:"rgba(232,234,246,.78)",whiteSpace:"pre-wrap",flex:1 }}>
                {baResult.split("\n").map((line,i)=>{
                  if(/^\d+\./.test(line)) return <div key={i} style={{ fontWeight:600,color:"#e8eaf6",marginTop:12 }}>{line}</div>;
                  if(line.startsWith("**")) return <div key={i} style={{ fontWeight:600,color:"#40c4ff" }}>{line.replace(/\*\*/g,"")}</div>;
                  return <div key={i}>{line}</div>;
                })}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* DESTINATIONS */}
      <section ref={destRef} style={{ ...S.sec, background:"#08081a" }}>
        <div style={S.label}>Where to go</div>
        <h2 style={{ ...S.h2,color:"#e8eaf6" }}>DESTINATIONS</h2>
        <div style={{ display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(260px,1fr))",gap:2,marginTop:44 }}>
          {Object.entries(DESTINATIONS).map(([key,d])=>{
            const daily = Object.values(d.budget).reduce((a,b)=>a+b,0);
            return (
              <DestCard key={key} d={d} name={key} daily={daily}
                onAsk={()=>{
                  const text=`Tell me everything a student needs to know about visiting ${key.charAt(0).toUpperCase()+key.slice(1)}, ${d.country} on a tight budget.`;
                  scrollTo(chatRef);
                  setTimeout(()=>sendMessage(text),600);
                }}/>
            );
          })}
        </div>
      </section>

      {/* FOOTER */}
      <footer style={{ background:"#04040c",color:"rgba(232,234,246,.28)",padding:42,textAlign:"center",borderTop:"1px solid rgba(124,106,255,.08)",position:"relative",zIndex:1 }}>
        <div style={{ fontFamily:"'Bebas Neue',sans-serif",fontSize:30,letterSpacing:".06em",color:"#e8eaf6",marginBottom:8 }}>
          Travel<span style={{color:"#7c6aff"}}>X</span>{" "}
          <span style={{ fontSize:14,color:"#7c6aff",fontFamily:"'Space Mono',monospace",letterSpacing:".1em" }}>AI</span>
        </div>
        <p style={{fontSize:13}}>Powered by {AUTHOR} · Built for student explorers · The world is big — go see it ✈️</p>
      </footer>
    </>
  );
}

// ── DESTINATION CARD ──
function DestCard({ d, name, daily, onAsk }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div onMouseEnter={()=>setHovered(true)} onMouseLeave={()=>setHovered(false)}
      style={{ background:hovered?"linear-gradient(135deg,#7c6aff,#40c4ff)":"rgba(255,255,255,.03)",border:"1px solid rgba(255,255,255,.05)",padding:26,cursor:"none",transition:"all .35s",position:"relative",overflow:"hidden" }}>
      <span style={{fontSize:34,display:"block",marginBottom:12}}>{d.emoji}</span>
      <div style={{ fontFamily:"'Bebas Neue',sans-serif",fontSize:26,letterSpacing:".04em" }}>{name.charAt(0).toUpperCase()+name.slice(1)}</div>
      <div style={{ fontSize:11,color:hovered?"rgba(255,255,255,.7)":"rgba(245,240,232,.4)",marginBottom:9 }}>{d.country}</div>
      <div style={{ fontSize:12,color:hovered?"rgba(255,255,255,.8)":"rgba(245,240,232,.48)",lineHeight:1.5 }}>{d.vibe}</div>
      <div style={{ marginTop:16,paddingTop:14,borderTop:`1px solid ${hovered?"rgba(255,255,255,.25)":"rgba(255,255,255,.07)"}`,display:"flex",justifyContent:"space-between",alignItems:"center" }}>
        <div style={{ fontFamily:"'Space Mono',monospace",fontSize:17 }}>~${daily}/day</div>
        <button onClick={onAsk} style={{ fontFamily:"'Space Mono',monospace",fontSize:9,textTransform:"uppercase",letterSpacing:".08em",background:hovered?"rgba(255,255,255,.22)":"rgba(255,255,255,.08)",border:"none",color:"#e8eaf6",padding:"6px 12px",cursor:"none",transition:"background .2s" }}>Ask AI →</button>
      </div>
    </div>
  );
}

// ── CUSTOM CURSOR ──
function CustomCursor() {
  const [pos, setPos] = useState({ x:-100, y:-100 });
  const [ring, setRing] = useState({ x:-100, y:-100 });
  const [big, setBig] = useState(false);
  useEffect(() => {
    const onMove = e => { setPos({ x:e.clientX, y:e.clientY }); setRing({ x:e.clientX, y:e.clientY }); };
    const onEnter = () => setBig(true);
    const onLeave = () => setBig(false);
    document.addEventListener("mousemove", onMove);
    document.querySelectorAll("button,a,select,input,textarea").forEach(el=>{
      el.addEventListener("mouseenter", onEnter);
      el.addEventListener("mouseleave", onLeave);
    });
    return () => document.removeEventListener("mousemove", onMove);
  }, []);
  return (
    <>
      <div style={{ position:"fixed",left:pos.x,top:pos.y,width:big?16:10,height:big?16:10,background:"#7c6aff",borderRadius:"50%",pointerEvents:"none",zIndex:9999,transform:"translate(-50%,-50%)",mixBlendMode:"screen",transition:"width .2s,height .2s" }}/>
      <div style={{ position:"fixed",left:ring.x,top:ring.y,width:big?48:32,height:big?48:32,border:"1.5px solid #7c6aff",borderRadius:"50%",pointerEvents:"none",zIndex:9998,transform:"translate(-50%,-50%)",transition:"left .1s ease-out,top .1s ease-out,width .3s,height .3s" }}/>
    </>
  );
}
