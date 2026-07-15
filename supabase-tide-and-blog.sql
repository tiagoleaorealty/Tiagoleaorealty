-- ═══════════════════════════════════════════════════════════════
--  1. Fill in TIDE Academy   2. Add the schools blog post (draft)
--  Run in Supabase > SQL Editor. Safe to re-run.
-- ═══════════════════════════════════════════════════════════════

-- ── TIDE Academy ──────────────────────────────────────────────
-- Every value below is from tideacademy.com (their /learning and
-- /admissions pages). Note the accreditation is scoped to grades 9-12
-- and comes via a partner school — it is not a whole-school US
-- accreditation, so it is worded that way on purpose.
UPDATE schools SET
  grades        = 'Pre-K – 12',
  curriculum    = 'Personalized US curriculum',
  languages     = 'English and Spanish',
  accreditation = 'Middle States Association (grades 9–12, via North Atlantic Regional High School)',
  founded       = '2011',
  excerpt       = 'Pre-K through 12 in Tamarindo on a personalized US curriculum — around 80 students from 17 countries at an 8:1 ratio, with high school accredited via Middle States through North Atlantic Regional High School.',
  meta_desc     = 'TIDE Academy, Tamarindo: Pre-K–12 personalized US curriculum, 8:1 student-teacher ratio, Middle States accreditation for grades 9-12. What relocating families should know.',
  body          = 'TIDE Academy is the school on this coast that does not look like the others, and that is the entire point.

Around 80 students from 17 countries, at an 8:1 student-teacher ratio. The school describes itself as built for students whose interests run past a conventional academic structure, and the model reflects that: one-on-one personalized education, adapted to each student, with a lot of the learning happening outside the classroom through internships at local businesses and community projects.

## What they teach

TIDE runs a personalized US curriculum from Pre-K through 12th grade — Pre-K and Kindergarten primarily in Spanish, then Grades 1–4, Grades 5–8, and high school.

For high school, accreditation comes through a partnership with North Atlantic Regional High School, which is accredited by Middle States Association of Colleges and Schools. That partnership covers grades 9–12.

The school reports a 95% college acceptance rate and 85% extracurricular participation.

## Who it fits

Families who want a small, flexible, deeply personal setup — and whose kid is the sort who does better with room to chase something than with a fixed timetable. If your child is already self-directed, TIDE tends to click quickly.

It is also worth being straight about the flip side. TIDE is not an IB school, and it does not publish as much detail as the bigger campuses do. If you want a large campus with extensive facilities and a heavily structured program, look at Journey, La Paz or CRIA first.

## Go see it

More than any other school here, TIDE is one you have to visit. The model is unusual enough that a website cannot tell you whether it fits your kid. Walk the campus, meet the teachers, and watch how the students actually spend a day.

---

*Details from TIDE Academy''s own published materials as of July 2026. Confirm current programs and accreditation directly with the school.*'
WHERE slug = 'tide-academy';

-- ── Blog post (draft — review before publishing) ───────────────
INSERT INTO blog_posts (title, slug, category, status, readtime, excerpt, meta_desc, body)
VALUES (
  'Schools on Guanacaste''s Gold Coast: A Guide for Relocating Families',
  'schools-guanacaste-gold-coast-guide',
  'lifestyle',
  'draft',
  '8 min read',
  'Every international, bilingual and private school on the Gold Coast — IB, Montessori, Waldorf and bilingual — plus the things that actually decide it: the drive, the waitlist, and why there are no school ratings in Costa Rica.',
  'A guide to international and bilingual schools in Guanacaste, Costa Rica — Journey, La Paz, CRIA, Del Mar, TIDE and more. Grades, curriculum and what relocating families need to know.',
  'Almost every family that calls me about moving to Guanacaste asks about the house first and the school second. Within a week, it has flipped. The school decides the town, the town decides the commute, and the commute decides which houses are even worth seeing.

So here is the honest version of what exists on the Gold Coast, and what nobody tells you until you are already here.

## First, the thing that surprises everyone

There is no GreatSchools here.

If you are coming from the US, you are used to opening a listing and seeing a 6/10 next to every nearby school. That number comes from state standardized testing. Costa Rica has no equivalent, and no independent body rates these schools on a comparable scale.

This matters more than it sounds. It means **anyone showing you a school score for Costa Rica invented it.** I would rather tell you what each school says about itself and let you do the visit than hand you a number I made up.

That is why the [schools page](https://soldbytiago.com/schools.html) on this site has no ratings. Grades, curriculum, languages, accreditation. Nothing else.

## The schools, by town

### Tamarindo and just inland

**[Journey School of Costa Rica](https://soldbytiago.com/school.html?slug=journey-school-tamarindo)** — Pre-K through 12, and an authorized IB World School, which is the credential most relocating families are scanning for. Also accredited through Middle States and part of the UNESCO Associated Schools Network.

**[TIDE Academy](https://soldbytiago.com/school.html?slug=tide-academy)** — the outlier, and deliberately so. Around 80 students from 17 countries at an 8:1 student-teacher ratio, built for kids whose interests run past a conventional academic structure. They publish very little about grades or curriculum, which tells you something about how they operate. Go see it.

**[Educarte](https://soldbytiago.com/school.html?slug=educarte)** — bilingual, MEP-certified, out toward Huacas. It is also the only school on this entire list that publishes its tuition: **$125 per month** for preschool and primary. Every other school on the coast makes you ask.

**[Pacífico Internacional](https://soldbytiago.com/school.html?slug=pacifico-internacional)** — Waldorf-inspired, preschool through middle school, up in the hills at Cañafistula. If Waldorf is your thing, this is the only option on this coast.

### Flamingo, Brasilito and Conchal

**[La Paz Community School — Cabo Velas](https://soldbytiago.com/school.html?slug=la-paz-community-school-cabo-velas)** — IB World School, PreK–12, dual-language immersion, sitting between Flamingo and Brasilito. Also accredited with ACEP and College Board. For a lot of families buying in Flamingo or Potrero, La Paz is the reason.

**[Costa Rica International Academy (CRIA)](https://soldbytiago.com/school.html?slug=costa-rica-international-academy)** — US-accredited and bilingual, on a 32-acre campus 500m south of Reserva Conchal. Founded in 2000, which makes it one of the longest-running international schools on the coast. If you want a US-track education, this is the anchor.

### Playas del Coco and the north

**[Dolphin''s Academy](https://soldbytiago.com/school.html?slug=dolphins-academy)** — bilingual elementary in Coco, with curricula developed in alliance with Oxford and Cambridge.

**[Lakeside International School](https://soldbytiago.com/school.html?slug=lakeside-international-school)** — PreK–12, bilingual, inland at Tablazo de Sardinal, built around an integrated Multiple Intelligences curriculum.

**[La Paz — Tempisque Campus](https://soldbytiago.com/school.html?slug=la-paz-community-school-tempisque)** — La Paz''s second campus, inland near Palmira in Carrillo, running the same IB dual-language program as Cabo Velas. Worth knowing about if you are looking around Papagayo.

### Nosara

**[Del Mar Academy](https://soldbytiago.com/school.html?slug=del-mar-academy)** — Pre-K through 12 on an 11-acre campus, running Montessori in the early years and finishing with the IB Diploma. Nosara is its own world, and Del Mar is a real part of why families commit to it.

## What actually decides this

### The drive is the whole thing

A school 12 km away is not 12 minutes away. Roads here bend around rivers, hills and the occasional herd of cattle, and in October some of them are worse than that. Families who skip this end up doing 50 minutes each way, twice a day, and they do not last.

**Drive it before you buy.** At 7am on a weekday, in the rain if you can manage it. Not at noon on a Sunday.

### There is no school bus system

Some schools run transport, some do not. Assume you are driving until a school tells you otherwise in writing. That single fact eliminates more houses than price does.

### IB is the export ticket

If there is any chance your kid finishes high school somewhere else, IB travels. On this coast that means Journey, La Paz (both campuses), and Del Mar. Not the only good option, but the one that keeps doors open.

### The waitlist is real

The good schools fill. Grades 6 through 9 are the tightest. Families arrive in July assuming they will sort school out in August and find nothing available until the following February.

**Call the schools before you shortlist towns.** Not after.

### MEP matters more than you think

MEP is Costa Rica''s Ministry of Education. MEP accreditation is what makes a diploma valid here. If there is any chance of your kid staying in the Costa Rican system, or of you needing local paperwork to line up cleanly, ask about MEP status directly.

## How to actually do this

1. Pick two or three schools based on curriculum, not on which town you liked on vacation.
2. Call them. Ask about openings in your kid''s exact grade for your exact start date.
3. Visit. All of them. In person. There is no rating to lean on, so the visit is the research.
4. Drive the route from the neighborhoods you are considering, at the hour you would actually drive it.
5. Then look at houses.

Families who do it in this order settle in. Families who buy the house first tend to be back on the market within two years, and I have listed a few of those.

## Where I come in

Every listing on this site shows the schools nearest to it, with distances. That is straight-line distance, so treat it as a starting point rather than a commute estimate.

If you tell me which school you are aiming at, I can work backwards to the neighborhoods that make that drive tolerable. That is usually a much shorter list than people expect, and it is a far more useful place to start than a price filter.

I grew up on this coast. I know which drives look fine on a map and are miserable in practice. Reach out at [tiago@soldbytiago.com](mailto:tiago@soldbytiago.com) and tell me the ages of your kids.

---

*Details on this page come from each school''s own published materials as of July 2026. Programs, tuition and accreditation change. Confirm everything directly with the school before you make a decision this size.*
'
)
ON CONFLICT (slug) DO UPDATE SET
  title = EXCLUDED.title, category = EXCLUDED.category, readtime = EXCLUDED.readtime,
  excerpt = EXCLUDED.excerpt, meta_desc = EXCLUDED.meta_desc, body = EXCLUDED.body;

-- Check
SELECT 'TIDE' AS what, grades, accreditation FROM schools WHERE slug = 'tide-academy'
UNION ALL
SELECT 'POST', status, title FROM blog_posts WHERE slug = 'schools-guanacaste-gold-coast-guide';
