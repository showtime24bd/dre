
# 🎮 Emote Image Addition Guide (বাংলায় গাইড)

## কিভাবে Emote Image যুক্ত করবেন

### পদ্ধতি ১: CDN Link ব্যবহার করে (সবচেয়ে সহজ)

আপনার `templates/index.html` ফাইলে, প্রতিটি emote এ `img` property যোগ করুন:

```javascript
'ak': { 
    id: '909000063', 
    icon: '🔫', 
    name: 'AK47',
    img: 'https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/909000063.png'
}
```

### পদ্ধতি ২: Local Image ব্যবহার করে

1. **Image Folder তৈরি করুন:**
   - `static` নামে একটি folder তৈরি করুন
   - এর ভিতরে `emote_images` folder তৈরি করুন

2. **Images রাখুন:**
   - আপনার সব emote images `static/emote_images/` এ রাখুন
   - File naming: `909000063.png`, `909042007.png` ইত্যাদি (emote ID দিয়ে)

3. **HTML এ path update করুন:**
```javascript
'ak': { 
    id: '909000063', 
    icon: '🔫', 
    name: 'AK47',
    img: '/static/emote_images/909000063.png'
}
```

### বর্তমান Image Sources:

আপনার `emotes_full.json` ফাইলে ইতিমধ্যে সব emote এর image URL আছে। এগুলো ব্যবহার করতে পারেন:

```json
{
  "id": "909000001",
  "name": "Hello!",
  "url": "https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/909000001.png"
}
```

### সহজ উপায়: Automatic Image Loading

আমি একটি script তৈরি করে দিচ্ছি যা automatically emotes_full.json থেকে images load করবে।

## Example: সব Weapon Emotes এ Image যোগ করা

```javascript
'Weapon Emotes': {
    'ak': { id: '909000063', icon: '🔫', name: 'AK47', 
            img: 'https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/909000063.png' },
    'm10': { id: '909000081', icon: '🔫', name: 'M10',
             img: 'https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/909000081.png' },
    'scar': { id: '909000068', icon: '🔫', name: 'SCAR',
              img: 'https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/909000068.png' }
}
```

## 📝 Important Notes:

1. **Image Format**: PNG বা JPG উভয়ই কাজ করবে
2. **Image Size**: 40x40px থেকে 100x100px ideal
3. **Fallback**: যদি image load না হয়, তাহলে emoji icon দেখাবে
4. **CDN Speed**: jsdelivr CDN ব্যবহার করলে fast loading হবে

## 🔧 Troubleshooting:

- Image দেখা যাচ্ছে না? Browser console check করুন (F12)
- URL ঠিক আছে কিনা verify করুন
- Image file size বেশি হলে compress করুন
