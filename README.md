# NewHope_X25519_XSalsa20_Poly1305
Post Quantum key exchange with NewHope and NaCl (requires Python3.6)
<hr>
(For the love of everything holy please do not use this yet. This is the very first version and many things will change.)<br>
The NewHope_X25519_XSalsa20_Poly1305 exchange class is found in the nhxpoly/ folderr.<br>
<br>
If NewHope turns out to be breakable, you will at least still have the same security X25519_XSalsa20_Poly1305 offers.<br>
Both algorithms need to be broken in order for the original exchange key to be reconstructed.<br>
Combining this key exchange with more public key algos will offer that much more security because then X amount of algos will have to be broken.<br>
With the resulting secret key from the exchange you may treat it as a OTP key and utilize the Vernam Cipher and exchange a new key per message.<br>
You can also use it to generate a AES-256 key. Recommendeded cipher modes would be CTR or GCM.<br><br>

<h1>Description</h1><br>
This library aims to combine the post-quantum NewHope encryption and X25519 elliptical curve cryptography.<br>
The key exchange takes place over two seperate encryption algorithms SIMILIAR but different to Google's CECPQ1 protocol using in Chrome Canary.<br>
First a random 32 byte key chunk is created by the software initiating the key exchange.<br>
The sender who wants to create the encrypted channels then creates a X25519_XSalsa20_Poly1305 key pair and sends it the exchange requester.<br>
The exchange requester encrypts the first 32 byte chunk and sends it back to the sender.<br>
This concludes the first half of the key exchange.<br> 
The requester then begins a commitment protocol which is essentially a way to verify that an eavesdropper isn't tampering with the NewHope key exchange.<br>
The sender sends a random shake_128 hashed seed to the requester.<br>
The requester stores this, then sends the requester their own unhashed seed.<br>
The sender then sends their unhashed seed and first sequence of the NewHope Basepoint.<br>
The requester verifies the seed matches the shake_128 hash.<br>
If so a the requester sends their NewHope Basepoint and an authentice NewHope Key exchange has taken place.<br>
Both the sender and requester can now generate their shared secret key.<br>
Both then combine the two shared key chunks to form a prekey.<br>
This key can now be used to start some sort of encrypted channel of the users choice.<br> 
 
Here is output from a test use of the protocol in example.py<br>
```
[Alice]: Prekey chunk created: [246, 249, 178, 233, 90, 176, 68, 123, 40, 78, 164, 188, 88, 201, 83, 215, 37, 12, 167, 91, 81, 84, 150, 71, 134, 13, 0, 28, 155, 106, 229, 184]
[Bob]: Created a X25519_XSalsa20_Poly1305 sealed box and sent public key to Alice
[Alice]: Encrypted prekey chunk using the recieved X25519 Public Key via unidentifiable authentication.
[Bob]: First prekey chunk decrypted [246, 249, 178, 233, 90, 176, 68, 123, 40, 78, 164, 188, 88, 201, 83, 215, 37, 12, 167, 91, 81, 84, 150, 71, 134, 13, 0, 28, 155, 106, 229, 184]
[Bob]: NewHope Seed commitment received with seed hash b'\xa6z\xba\x88\xe7\xb0\xaf\n\xec6\x9e\xbb\x83\x12[6)i\x9f\x18\xdd\nZ^\xbcyG\x96  U\xe6\x1d\x1f\x80\x14\xb5G\x13k:!u.g\xcc\x88\xa1\xdcX\x95\xd0\xdd\xcbO=\xf3\xa4\xe6\x93hC\xca9t\xf5\x7f\xe4\x0f\x1d~\xe7\x93\x11xPU\xbaU\x10\r\x07\x8f\xf8H\xbct\xdb\x0f\xb0\xd0D{xg\x9b\xe4\x8e\xe0\xf5'
[Alice]: NewHope initial message exchange sent
[Bob]: Seed verification succeded. Authentic NewHope message recieved
[Alice]: Recieved final NewHope message
[Bob]: NewHope shared key [191, 178, 30, 43, 31, 35, 94, 65, 96, 174, 186, 240, 173, 159, 110, 133, 27, 123, 113, 147, 112, 95, 241, 108, 210, 57, 145, 199, 3, 36, 242, 81]
[Alice]: NewHope shared key [191, 178, 30, 43, 31, 35, 94, 65, 96, 174, 186, 240, 173, 159, 110, 133, 27, 123, 113, 147, 112, 95, 241, 108, 210, 57, 145, 199, 3, 36, 242, 81]
[Bob]: Combined prekey [191, 178, 30, 43, 31, 35, 94, 65, 96, 174, 186, 240, 173, 159, 110, 133, 27, 123, 113, 147, 112, 95, 241, 108, 210, 57, 145, 199, 3, 36, 242, 81, 246, 249, 178, 233, 90, 176, 68, 123, 40, 78, 164, 188, 88, 201, 83, 215, 37, 12, 167, 91, 81, 84, 150, 71, 134, 13, 0, 28, 155, 106, 229, 184]
[Alice]: Combined prekey [191, 178, 30, 43, 31, 35, 94, 65, 96, 174, 186, 240, 173, 159, 110, 133, 27, 123, 113, 147, 112, 95, 241, 108, 210, 57, 145, 199, 3, 36, 242, 81, 246, 249, 178, 233, 90, 176, 68, 123, 40, 78, 164, 188, 88, 201, 83, 215, 37, 12, 167, 91, 81, 84, 150, 71, 134, 13, 0, 28, 155, 106, 229, 184]
NewHope_X25519_XSalsa20_Poly1305 key exchange successful.
```
<br>
I've added an example implementation that uses your network via Twisted todo the key exchange.<br>
There's a rendezvous server to directly link two clients p2p via UDP hole punching.<br>
So the key exchange takes place with no middle man.<br>
Here's how you can test it: (Run each command in a seperate console/terminal window<br>

```
python3.6 twisted_server.py 
python3.6 twisted_client.py r
python3.6 twisted_client.py s
```

<br>
Here is output from the key exchange requester client (the command which has the 'r' argument in it)

```
Successfully connected to rendezvous server
Sent init to 127.0.0.1:58642
Sent NewHope_X25519_XSalsa20_Poly1305 init
2
Recieved X25519_XSalsa20_Poly1305 Sealed Box Key b'ld\xdf\x0b\xbaB}\xc5\x82\x16\xd7\x08\xba\xe1\xbfZ\xad\xa1\x8az\xe1\x94\x95\xcbB\xfb \xdd\x13a^\x02'
Prekey chunk 1: b"\xc9\xe5\x83\x06h\xdb\xd5\x80\x16\x97&\xf3x\xf8\x8c\xf2'\xc9\xd8\x13\x05oi}\xf6\xc4\x93\x01vH\x03N"
Sent encrypted prekey chunk 1
4
Recieved NewHope commitment hash: b'\xafK\xe5\x9fCR\x1c\xcd\xb5./=\xbe\xba\x18\xa6\xad\xe4\xf1.xt\x00\xa2\xd9\x84]\xadS\x1d\r\xaa\xde+\xf7y\xca[S\xc0\xbc\xd5\x99\xd1\r\xed\xab\xb1\xfa\xa9\xaf\x06@\xf5\x8dA\xfc\x84\x98M\xf7/E\xd2(\xf5;<V\x15B\xdaI\xd6\x06\x8f+\xd4yI\xad\x90\xfc:Y\x873\xfap0+{\x1a\x1b\xf1\xf5\xbbG@\x1c'
Sent NewHope raw commitment seed: b'3.>*\x86.I\x1e@^em\xecZuWTC\xcb\xc0p\xa9"\xf8\x88*5o\xac\x03\x9c\x8d\xd3NPG;"\x18Bl~\xe8\x1f\xd7W\xff\xb6\x08\xcb\x9b\x87tZ\xc0\x89[n]F\x1b\xb8\xe1\xe91\\\x05\xb7\x11\x8e\x0c/\x9d\xe0U\nR\x19\xc6\xfaQ\xde\x9bV\x9d\x04\xdd\xdd+\xf1\xa4\x99l\x85*@T/\xb4K\xa1\xb6#\x11*m\xa5\xcc\x84zS\xdai\xf4\x93\xfbo&\xdc\xbc\xd8\x90\x854+E\xa9\x17:$\x94\xe7\x82\xa8SI\xe0o7\x13\x80\x0c1\xb8\xfa\xd1\x88J\xe3\xb7R\xd2\xcev\x97\xbe\x8a\xcc^K\xac\'A\x86s\x8c\xc2q\x14\xedA8\x85\xf4\x9d+\x02\xf3\xfa\x89\xf8\xbf\xfbk\xa1\xe6\x16\xbd\xdeJDp\x15X\xb9\xab\xe1\x03\xbc\xc6\x96\x0f\xc2\x8c\xbc\xa8t\xc1\t\x83\x186\t`\xc8! P\xf5$ \xd5.d\x94\xb7\x81\x815\xfa\xe4uv\xfdC\x95\xfdi\xc6\xd4\x11\xe5\xd6\xa9^\x10\x92\x08\x80\xc7\xd5\x03\xa3<2\xe4\xa8\xdd\xa4GA7>D\xd9\x94\xe8\xb5]B^ \x96\x086u\x0e;\xaa\x0b\xbf^\xf1T>{C\xd8\xcf"\xf1\xf5\xa1\x9d>\x02\x14n\x94\x07p\xe0\x03G\xed?3C)\xbe\x91?\xa9r\xdd\x8d\xe9\xc7/:\x10+}\xd1\x9c\x16\xef\x8cZ\xf9\xbdu\xf7XPc\x9fO=CPdry\x9b,D\xe6\x16x\x97\x06\xfcd\xce(H\x8d\xf3\x91\x85\xe9\xe5\x9d\xdd\x89\xc7\x9d\xe5a\x98\x15 \xb3\x0f(\x16\rq\xd9\x8f\xab\x146N\xf4\\\x98p\xa1\x83R;\xb2\xf4\xb6\xce\xac\x836\x10\xd0O\x97^U`\xbb\x86>OoS\xa3/\xb4\xf0Qy-oF\xcb\x86U\x126\xf6\xddf\'0\xfe\x83{\xd1?-\xdd"\xba4\x18\xb2a\xf2\xff\xdd\x13\xe4)\xbcO\x99\x15+M\x96\xbb\xf8\x18\xa3\xe5M\xa1\xfcx#\x99\x1e\xbf9\xf5k\xbe\xfd\x95\xc7fV\xe6\xd4\xf6\xb7\xc9\x8b\x130\x98\xc9\xdd\x9d\xec*b\xf1)s\xef\x02Z\x04\xf9]"V\x1e#\xce\xe8\xf0\xfdo\x9a\xd0\x0e\xc6^\xe2\x02#y6\xb0d\x13c\xea\xde\xcaA ='
6
Seeds verified
8
Received NewHope message: ([6555, 8917, 8195, 2807, 5577, 1630, 4764, 12371, 1549, 12550, 6190, 7873, 7717, 7313, 12258, 11255, 826, 3512, 5190, 9214, 12514, 11072, 3378, 1301, 9974, 4953, 5478, 10084, 8589, 11807, 11460, 11491, 2056, 10115, 8022, 9273, 5011, 7857, 3245, 4389, 10088, 5216, 6105, 1920, 5164, 1457, 6096, 10689, 4385, 11771, 4321, 8920, 868, 1667, 9880, 3712, 10395, 9599, 993, 7868, 11370, 3139, 1922, 7330, 6726, 10097, 7996, 3974, 2534, 10763, 8984, 4854, 11391, 8733, 8532, 11221, 1900, 3119, 2139, 2349, 3933, 12970, 8283, 7864, 7552, 7134, 6309, 3698, 3923, 12546, 11441, 5245, 4347, 8601, 8630, 8509, 9531, 5573, 1654, 11313, 7725, 11273, 8372, 2161, 5906, 7392, 7208, 6641, 6484, 12571, 12998, 11873, 10015, 9430, 7920, 7790, 7546, 3784, 2198, 7372, 9381, 5456, 1687, 11265, 3938, 7683, 6088, 6986, 7166, 8867, 7964, 1275, 6252, 854, 7717, 3194, 1483, 4042, 7977, 10179, 7813, 11634, 9970, 4274, 11467, 5234, 5703, 8794, 6492, 7304, 12651, 6206, 3047, 5565, 8673, 4712, 12433, 6402, 7612, 12194, 2734, 12701, 3914, 6841, 2124, 7041, 1879, 2521, 1988, 12298, 8970, 2334, 8639, 5070, 8553, 2280, 13072, 10425, 8696, 2199, 1784, 1594, 12816, 3311, 13043, 10577, 8546, 13386, 6720, 993, 11209, 12349, 5535, 7615, 7906, 8887, 11706, 1821, 858, 3979, 6691, 11618, 5818, 2406, 3704, 13078, 5450, 7111, 12397, 9897, 13382, 11767, 9782, 9329, 8808, 11351, 6183, 2336, 11924, 13006, 7606, 12934, 6814, 11613, 1950, 4822, 2069, 10654, 3488, 12237, 3774, 2991, 2288, 3348, 9622, 5579, 1122, 5700, 2738, 1280, 8202, 3252, 6819, 5432, 6961, 1498, 3547, 10051, 4595, 5753, 11054, 6924, 11243, 6093, 13058, 2989, 4561, 5956, 12255, 12086, 9254, 6651, 7948, 3386, 8866, 4511, 3167, 9751, 10785, 4988, 11583, 2868, 7350, 13085, 7847, 3792, 2114, 12594, 11653, 7558, 7960, 11117, 6182, 1749, 1531, 8894, 3385, 5538, 12029, 7194, 1965, 11074, 9769, 1220, 5545, 6249, 6479, 10568, 10586, 12410, 4390, 9492, 6601, 12737, 12267, 1328, 12248, 6914, 9014, 11922, 7341, 5048, 3884, 3373, 10552, 1393, 12190, 4130, 1349, 12252, 2187, 4924, 5476, 10695, 10755, 11332, 8306, 12407, 1383, 1681, 11587, 7480, 1634, 8548, 12223, 1022, 6211, 9387, 3192, 7108, 5800, 9557, 9804, 2845, 10581, 9366, 10015, 2852, 8250, 13014, 2610, 11374, 9416, 12028, 5151, 10728, 5179, 1632, 8788, 11187, 2007, 12176, 6359, 7389, 12939, 6087, 8596, 4079, 7940, 1406, 4491, 13014, 7277, 8677, 4601, 6524, 10637, 8969, 10424, 9437, 4941, 8758, 1502, 4133, 11367, 4861, 7835, 11032, 10239, 6011, 7982, 8703, 5003, 7576, 5351, 9289, 5245, 7566, 2175, 4168, 9185, 10488, 8115, 5026, 6700, 10818, 2441, 9692, 1464, 12419, 8858, 3285, 7555, 1569, 10564, 12526, 7107, 9189, 8235, 8514, 12001, 3256, 4727, 5828, 3621, 5978, 5429, 10531, 1998, 5310, 12098, 8118, 11328, 6411, 12425, 8705, 6327, 1519, 10334, 11342, 8610, 9068, 9619, 10921, 10133, 2167, 8224, 8527, 10093, 6471, 12621, 4839, 12286, 10173, 3183, 2642, 8534, 2552, 7418, 2888, 8934, 10094, 1583, 6168, 3650, 3428, 5318, 5832, 855, 5771, 7002, 1775, 4284, 11525, 12006, 9915, 7267, 1231, 1652, 4568, 10575, 9390, 3384, 11823, 12946, 3111, 7694, 8751, 5806, 7204, 10410, 9851, 7753, 12984, 12807, 7344, 1964, 3739, 11909, 12933, 10911, 1408, 3869, 5986, 2394, 11889, 4060, 1726, 5881, 12286, 2780, 2911, 5968, 10584, 1251, 5916, 12679, 4944, 3210, 12668, 896, 8685, 1323, 6604, 9151, 7536, 6120, 9245, 9340, 12385, 10543, 3445, 12973, 4630, 3796, 12641, 1276, 4784, 1779, 11789, 5196, 2319, 4682, 11845, 4273, 11024, 10282, 3281, 4721, 8751, 11781, 1982, 5465, 10159, 863, 11457, 5076, 7100, 5248, 6125, 12622, 3131, 6995, 3078, 6704, 1093, 10103, 3365, 5091, 12367, 8284, 1976, 11789, 11081, 7010, 4166, 922, 10975, 11927, 8225, 3157, 9844, 7309, 8129, 2356, 9669, 6342, 4172, 11660, 9409, 12758, 2476, 3619, 11736, 10715, 11402, 9401, 1877, 4924, 4191, 4188, 9072, 9311, 3671, 6607, 2606, 3855, 7085, 3965, 5185, 10668, 11000, 10162, 12727, 1202, 6881, 7526, 5031, 2887, 8641, 8114, 1009, 7918, 9340, 10488, 6538, 8664, 13038, 12976, 7576, 4018, 3380, 3644, 6764, 9068, 11887, 2921, 1923, 10341, 6740, 3658, 4031, 7873, 7873, 4319, 8886, 6877, 853, 2318, 12114, 6788, 3539, 9828, 5054, 3028, 8621, 2257, 9884, 2730, 9614, 10076, 3409, 4008, 12815, 12476, 8495, 12868, 6172, 10540, 3071, 10711, 12551, 9418, 1825, 12721, 12864, 3533, 4731, 10774, 7916, 8012, 11107, 10312, 3030, 4865, 11416, 5886, 10431, 2298, 6838, 7332, 7917, 4988, 8667, 4921, 1461, 11894, 3445, 11720, 5466, 3612, 6127, 4282, 3292, 3393, 3858, 1218, 1888, 2583, 9347, 5918, 5350, 11649, 3173, 3413, 2439, 2063, 12938, 11683, 12001, 1803, 8499, 5356, 3714, 1354, 1897, 2808, 3354, 11686, 12609, 5143, 8901, 12557, 8036, 3683, 9428, 1956, 2903, 12178, 5836, 1300, 10528, 12725, 9430, 6636, 12865, 7256, 12062, 12727, 10458, 5455, 12541, 6946, 2608, 1254, 1721, 2729, 1865, 11740, 6767, 6295, 7557, 5569, 6000, 2925, 4440, 11607, 1483, 5682, 2629, 6318, 1589, 3788, 3375, 3498, 12346, 12098, 2930, 8764, 2307, 4732, 2773, 5253, 5029, 1004, 6928, 4815, 6477, 1951, 1766, 5013, 13005, 11582, 6174, 3753, 4139, 9473, 3757, 10437, 6638, 5131, 11614, 11628, 8539, 10787, 4160, 10757, 4626, 1108, 6021, 2113, 1980, 7777, 3797, 10410, 5401, 3876, 1079, 3064, 2745, 10594, 10794, 10134, 9876, 4652, 7548, 6054, 2107, 1250, 10633, 1215, 6226, 8867, 11779, 1872, 4290, 9231, 6118, 9692, 10303, 3274, 1119, 8568, 9178, 5471, 10557, 1158, 8996, 824, 2104, 6515, 8896, 8762, 9437, 1565, 2123, 7536, 6965, 1704, 8223, 2329, 10912, 5679, 6523, 7246, 8510, 4185, 2170, 7646, 9249, 10203, 3859, 5547, 3924, 3351, 998, 13053, 1932, 8455, 4712, 12518, 1744, 7951, 8060, 2073, 12754, 2691, 7587, 7116, 6381, 10352, 3847, 6662, 6352, 12557, 2663, 1575, 11111, 10093, 1602, 8184, 8219, 9668, 10303, 8515, 8391, 1307, 6953, 2537, 1168, 8931, 10893, 2580, 996, 10457, 7222, 10839, 6636, 3875, 7715, 10458, 5568, 2674, 11547, 6639, 4925, 8062, 10081, 1456, 5348, 5805, 1913, 5402, 6584, 9142, 1680, 8648, 6317, 4960, 9448, 11133, 10596, 10356, 9515, 7653, 9701, 4804, 3667, 1058, 6015, 8854, 12811, 1635, 10226, 1437, 12488, 8647, 11628, 4039, 9783, 8580, 3762, 1185, 8210, 1006, 2537, 3798, 11841, 9363, 5001, 9255, 11922, 4252, 4347, 8728, 11053, 1663, 11255, 5787, 8918, 1653, 12585, 6600, 6335, 10546, 5951, 8862, 6467, 6899, 3027, 6092, 11757, 4955, 9131, 8110, 9261, 942, 1602, 5626, 9266, 7064, 5225, 2728, 2031, 972, 9746, 9313, 5011, 12894, 6224, 7659, 4866, 7330, 8010, 9589, 3042, 9317, 9707, 6547, 6382, 6036, 10825, 11685, 2239], b'\x81\xbd\x872\xd7Z\x9b\x14\xd4|\x8cj\xa9\xee\xb1/r-HY\xde\x08(IT\xb1\xa8\x81-\xa49\xd5')
Shared key: [185, 64, 226, 112, 169, 8, 188, 226, 91, 70, 24, 170, 174, 203, 207, 35, 55, 150, 123, 43, 95, 172, 252, 39, 215, 84, 58, 10, 106, 60, 206, 225]
Combined prekey: [185, 64, 226, 112, 169, 8, 188, 226, 91, 70, 24, 170, 174, 203, 207, 35, 55, 150, 123, 43, 95, 172, 252, 39, 215, 84, 58, 10, 106, 60, 206, 225, 201, 229, 131, 6, 104, 219, 213, 128, 22, 151, 38, 243, 120, 248, 140, 242, 39, 201, 216, 19, 5, 111, 105, 125, 246, 196, 147, 1, 118, 72, 3, 78]

```

<b>Warning</b>
This is the bare minimum possible implementation in twisted. There is no packet structure. Possible errors that will crash twisted as well.<br>
