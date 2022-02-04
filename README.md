# VocaTester
> 단어 암기에 도움을 주는 테스트 생성 및 관리 프로젝트.

이 프로젝트는 단어 암기에 도움을 주는 몇가지 유형의 테스트를 생성해줍니다. 사용하기 쉬운 엑셀을 활용하여 단어 데이터를 저장 및 활용하도록 하여 사용자가 임의로 수정하기 편하도록 하였습니다. 

오답을 확인 및 점검하고, 더이상 오답이 발생하지 않을 때까지 오답을 반복해서 테스트합니다.

누적된 테스트의 데이터를 활용하여 샘플을 추출하여 테스트를 진행할 수 있고, 누적된 오답들을 활용하여 테스트를 진행할 수 있습니다.

## 설치 및 실행 방법

[releases]의 exe파일을 다운로드 받아서 실행하거나 다음의 과정을 통해 설치 및 실행합니다.

```sh
git clone https://github.com/KangInPark/VocaTester.git
pip install pyqt5
pip install openpyxl
python .\VocaTester\main.py
```
## 설치 요구사항

설치를 통해 직접 실행할 경우 다음이 요구됩니다.
* Python3
* PyQt5 >= 5.15.6
* openpyxl >= 3.0.9

## 사용 예제

### 엑셀 파일 작성

학습할 단어를 엑셀 파일에 작성하여야 합니다.

||A|B|C|
|:-:|:-:|:-:|:-:|
1|단어1|단어1의 품사|단어1의 뜻
2|단어2|단어2의 품사|단어2의 뜻
3|단어3|단어3의 품사|단어3의 뜻

의 형식으로 작성하면 됩니다.

_예시_

![image](https://user-images.githubusercontent.com/62737791/152538352-12ecf383-32ba-43a1-8e0b-eea2905f49c6.png)

### 실행

**오늘의 단어 테스트**와 **누적 테스트**의 두 가지 버튼이 존재하며, **누적 테스트**의 경우 **오늘의 단어 테스트**를 통해 저장된 단어 데이터(누적, 오답)가 있을 때 활성화됩니다.

<img src ="https://user-images.githubusercontent.com/62737791/152534136-9d4cde3a-8b4b-4b3b-9d21-2b00bf096998.png" width=50%>

### 오늘의 단어 테스트

테스트 생성에 필요한 옵션을 지정합니다. **단어 파일 선택 버튼** 을 통해서 만들어둔 '.xlsx'파일을 선택합니다.

이후 **시작** 버튼을 통해서 테스트를 진행합니다.

<img src ="https://user-images.githubusercontent.com/62737791/152536193-96b01672-2114-43d0-8bc2-ad689c6fdaae.png" width=50%>

### 문제 유형

세 가지의 문제 유형을 선택할 수 있습니다.

설정에서 지정한 제한 시간을 초과하면 자동으로 오답으로 처리되며 안내 팝업창이 나타납니다.

* 단어 맞추기
  
<img src ="https://user-images.githubusercontent.com/62737791/152534242-17ede960-d77e-4e75-b98a-07d6b5fa8042.png" width=50%>

* 단어보고 뜻 고르기
  
<img src ="https://user-images.githubusercontent.com/62737791/152534200-aa7ba5d7-5120-46ff-a4d1-a12424d1bf72.png" width=50%>

* 뜻보고 단어 고르기
  
<img src ="https://user-images.githubusercontent.com/62737791/152534277-75f95c31-c88b-4496-af16-27fb8c2ab2fa.png" width=50%>

### 누적 테스트

누적 테스트에 필요한 옵션을 지정합니다. 

**누적 단어**는 현재까지 오늘의 단어 테스트를 통해 축적한 단어 데이터를 활용하여 테스트를 진행합니다.

**오답 단어**는 현재까지 테스트를 통해 축적한 오답 데이터를 활용하여 테스트를 진행합니다.

범위 설정에서 날짜별로 관리된 데이터의 범위를 지정할 수 있습니다. 문제 개수만큼 테스트를 진행합니다.

<img src ="https://user-images.githubusercontent.com/62737791/152534401-4a8a8ada-d279-4d43-a429-ee49eefd0237.png" width=50%>

### 오답 점검

테스트가 한 차례 끝난 후 오답이 있다면 오답 점검으로 넘어갑니다. 오답 점검 화면에서 사용자가 작성한 오답도 확인할 수 있습니다. **단어보고 뜻 고르기**, **뜻보고 단어 고르기** 유형의 경우 사용자가 선택한 선택지를 알려줍니다.

<img src ="https://user-images.githubusercontent.com/62737791/152534326-9697428c-b366-46fd-bb1e-583b2f5065b0.png" width=50%>

### 기타

테스트는 오답이 발생하지 않을 때까지 계속해서 반복되며, 매번 옵션을 다르게 설정할 수 있습니다. 'X'버튼을 통해 테스트 혹은 오답 점검을 중간에 종료할 수 있습니다.

오늘의 단어 테스트를 진행하였다면 '\data' 경로에 'CumulativeWords.xlsx', 'review.xlsx', 'Wdata.pkl' 파일이 생성됩니다. 

'CumulativeWords.xlsx'파일에는 누적된 단어가 날짜별로 시트를 구분하여 작성되어 있습니다.

'review.xlsx'파일에는 오답 단어가 날짜 및 테스트 회차별로 시트를 구분하여 작성되어 있습니다.

'Wdata.pkl'파일은 문제 유형에 따른 보기 생성에 활용되는 데이터 파일입니다.

## 정보

박강인(KangIn Park) – pkizone1@gmail.com

VocaTester는 오픈소스 소프트웨어로 GPL-3.0 라이센스를 준수하며 ``LICENSE``에서 자세한 정보를 확인할 수 있습니다.

[https://github.com/KangInPark/VocaTester/blob/master/LICENSE](https://github.com/KangInPark/VocaTester/blob/master/LICENSE)

<!-- Markdown link & img dfn's -->
[releases]: https://github.com/KangInPark/VocaTester/releases
